import MySQLdb as mysql
from flask import (Flask, g, request, session, render_template, redirect, 
                   url_for, flash, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

from datetime import datetime

# setup our Flask program
program = Flask(__name__)
program.config.from_object('settings')
program.config['DEBUG'] = True


# Decorator for view functions. Checks whether there is a user_id in the 
# current session. If not, redirects to login page. If so, runs the view 
# function.
def login_required(f):
    @wraps(f)
    def dec_fn(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return dec_fn

# The index. If a user is not logged in, then we prompt them to log in or 
# register. If they are logged in, we check their user type and redirect them
# appropriately.
@program.route('/')
def index():
    # user is not logged in
    if not session.get('user_id'):
        # open a cursor to the database
        cursor = g.db.cursor()
        cursor.execute("""SELECT T.team_id, T.school, S.name FROM Team T, plays P, Sport S
                        WHERE T.team_id = P.team_id AND P.sid = S.sid 
                        ORDER BY T.school""")
        teams = cursor.fetchall()
        return render_template('login.html', teams=teams)

    user_id = session['user_id']
    if session['user_type'] == 'coach':
        return redirect(url_for('coach_info', user_id=user_id))
    elif session['user_type'] == 'athlete':
        return redirect(url_for('athlete_info', user_id=user_id))

### Coach views ###

# Displays information about a coach including teams coached.
@program.route('/coach/<int:user_id>')
@login_required
def coach_info(user_id):
    cursor = g.db.cursor()

    cursor.execute("""SELECT C.team_id, T.school FROM coaches C, Team T
                    WHERE C.user_id=%s AND C.team_id=T.team_id""", (user_id,))
    teams = cursor.fetchall()

    # if we are requesting our own page, then we want to show them the pay
    if user_id == session['user_id']:
        cursor.execute('SELECT pay FROM Coach WHERE user_id = %s', (user_id,))
        pay = cursor.fetchone()[0]
    # otherwise, that is privileged information
    else:
        pay = None
    
    return render_template('coach.html', pay=pay, teams=teams, user_id=user_id)


### Team views ###

# Displays information about a team, like the team roster. If you are the 
# coach of this team, then displays the recent workouts and allows you to 
# create a new workout
@program.route('/team/<int:team_id>')
@login_required
def team_info(team_id):
    cursor = g.db.cursor()
    # general team information
    cursor.execute("""SELECT T.school, T.hometown, S.name 
                      FROM Team T, Sport S, plays P
                      WHERE T.team_id = %s AND S.sid = P.sid  """, 
                      (team_id,))
    team = cursor.fetchone()
    cursor.execute('SELECT mascot FROM TeamMascot WHERE school=%s',
                    (team[0],))
    mascot = cursor.fetchone()[0]

    # get teammates of the team
    cursor.execute("""SELECT U.user_id, M.number, U.name, M.position
                      FROM User U, member_of M
                      WHERE M.team_id = %s AND M.user_id = U.user_id
                      ORDER BY M.number""", (team_id,))
    teammates = cursor.fetchall()

    cursor.execute('SELECT user_id FROM coaches WHERE team_id = %s', (team_id,)) 
    # The cursor always returns tuples, so for a single value we just unpack
    # it
    coaches = map(lambda (x,) : x, list(cursor.fetchall()))

    # If multiple coaches, we want them all to be able to see the workouts
    coach = True if session['user_id'] in coaches else False

    cursor.execute("""SELECT workout_id, date_assigned 
                      FROM Workout 
                      WHERE team_id=%s
                      ORDER BY date_assigned DESC
                      LIMIT 5""", 
                  (team_id))

    workouts = cursor.fetchall()

    return render_template('team.html', team=team, 
                                        teammates=teammates,    
                                        coach=coach,
                                        workouts=workouts, mascot=mascot,
                                        team_id=team_id)

# Allows a coach to create a workout for a given team.
@program.route('/team/<int:team_id>/workout/create')
@login_required
def create_workout(team_id):
    cursor = g.db.cursor()
    cursor.execute('SELECT user_id FROM coaches WHERE team_id = %s AND user_id=%s', 
                   (team_id, session['user_id'])) 
    # if the coach does not coach this team, we do not want them to be
    # able to create workouts for them, so we redirect.
    if int(cursor.rowcount) == 0:
        flash('You don\'t have permission to do that', 'error')
        return redirect(url_for('team_info', team_id=team_id))

    cursor.execute('SELECT DISTINCT muscle_group FROM ExerciseMuscles')
    muscles = cursor.fetchall()
    print muscles

    return render_template('create.html', muscles=muscles, team_id=team_id)

# Endpoint for workout form submission. This is actually called asynchronously
# from the workout creation endpoint.
@program.route('/team/<int:team_id>/workout/submit', methods=['POST'])
@login_required
def submit_workout(team_id):
    cursor = g.db.cursor()
    cursor.execute('SELECT user_id FROM coaches WHERE team_id = %s AND user_id=%s', 
                   (team_id, session['user_id'])) 
    # if the coach does not coach this team, we do not want them to be
    # able to create workouts for them, so we redirect.
    if int(cursor.rowcount) == 0:
        return jsonify(error='You don\'t have permission to create a workout for this team')
    
    #print request.form['workout[0][exercise]']

    cursor.execute('INSERT INTO Workout(team_id, date_assigned, user_id) VALUES (%s, %s, %s)',
                    (team_id, datetime.now(), session['user_id']))
    
    # since Workout ids are auto incremented, we get the workout_id for the one we just created
    workout_id = cursor.lastroworkout_id

    # associate the exercises with the newly created workout
    for i in range(len(request.form)/3):
        cursor.execute('SELECT eid FROM Exercise WHERE name=%s',
                        (request.form['workout[%d][exercise]'%i]))
        eid = cursor.fetchone()[0]
        sets = request.form['workout[%d][sets]'%i]
        reps = request.form['workout[%d][reps]'%i]
        cursor.execute('INSERT INTO consists_of VALUES (%s, %s, %s, %s)',
                        (workout_id, eid, sets, reps))

    # commit the transaction
    g.db.commit()
    return jsonify(success=True)


# Displays the exercises in the workout. Also uses a stored procedure
# to determine which teammates on the team have and have not completed the workout
@program.route('/team/<int:team_id>/workout/<int:workout_id>')
@login_required
def workout_info(team_id, workout_id):
    cursor = g.db.cursor()
    cursor.execute('SELECT date_assigned FROM Workout WHERE workout_id=%s',(workout_id,))
    date = cursor.fetchall()[0][0]

    # get the exercises associated with this workout
    cursor.execute("""SELECT E.eid, E.name, C.sets, C.reps
                      FROM Exercise E, consists_of C 
                      WHERE C.workout_id = %s AND E.eid = C.eid""", (workout_id,))
    exercises = cursor.fetchall()

    # call the stored procedure. See schema.sql for details
    cursor.callproc("TeamProgress", (team_id,workout_id))
    teammates = cursor.fetchall()

    return render_template('workout.html', exercises=exercises, 
                                           teammates=teammates, 
                                           date=date,
                                           workout_id=workout_id)

# This endpoint is used by the workout creation view. It is called 
# asynchronously using ajax. Given a muscle group, it returns all exercise
# names associated with that muscle group.
@program.route('/exercises')
def exercises():
    muscle = request.args.get('muscle')
    cursor = g.db.cursor()
    # if they select any, then we just return all exercises
    if muscle == 'any':
        cursor.execute('SELECT name FROM ExerciseMuscles')
    else:
        cursor.execute('SELECT name FROM ExerciseMuscles WHERE muscle_group=%s',
                    (muscle,))
    # unpack the tuple
    e = map(lambda (a,) : a, list(cursor.fetchall()))
    # jsonify serializes the list and returns it with a json mimetype
    return jsonify(exercises=e)

### Athlete views ###

# Shows an athlete's performance for a given workout
@program.route('/athlete/<int:user_id>/workout/<int:workout_id>')
@login_required
def athlete_performance(user_id, workout_id):
    cursor = g.db.cursor()
    # get general info about the user
    cursor.execute('SELECT U.user_id, U.name FROM User U WHERE U.user_id = %s', (user_id,))
    user = cursor.fetchone()
    # if it's the current user, we make note of that. This variable is used
    # in the template to decide whether to allow input
    if user[0] == session['user_id']:
        is_self = True
    else:
        is_self = False

    cursor.execute('SELECT date_assigned FROM Workout WHERE workout_id=%s',(workout_id,))
    date = cursor.fetchone()[0]

    # essentially used to see whether the athlete has completed the workout
    cursor.execute('SELECT * FROM does D WHERE D.user_id=%s AND D.workout_id=%s',
                    (user_id,workout_id))
    # athlete has not completed workout
    if cursor.rowcount == 0:
        completed = False
        cursor.execute("""SELECT E.name, C.reps, E.eid
                        FROM Exercise E, consists_of C
                        WHERE C.workout_id = %s AND E.eid = C.eid""",
                        (workout_id, ))
        exercises = cursor.fetchall()
    else: 
        completed = True
        # if completed, we query the performance table instead
        cursor.execute("""SELECT E.name, P.max_weight
                        FROM Exercise E, performance P
                        WHERE P.user_id = %s AND P.workout_id = %s AND E.eid = P.eid""",
                        (user_id, workout_id))
        exercises = cursor.fetchall()

    # get team_id for link to teams workout page
    cursor.execute('SELECT team_id FROM Workout WHERE workout_id=%s', (workout_id,))
    team_id = cursor.fetchone()[0]

    return render_template('performance.html', user=user,
                           exercises=exercises, date=date, team_id=team_id,
                           workout_id=workout_id, is_self=is_self, completed=completed)


# General information about an athlete
@program.route('/athlete/<int:user_id>')
@login_required
def athlete_info(user_id):
    cursor = g.db.cursor()
    # get general info about athlete
    cursor.execute("""SELECT U.name, A.height, A.weight 
                      FROM User U, Athlete A 
                      WHERE U.user_id = A.user_id AND U.user_id = %s""", (user_id,))
    athlete = cursor.fetchone()

    cursor.execute("""SELECT M.team_id, T.school FROM member_of M, Team T
                        WHERE M.user_id=%s AND M.team_id=T.team_id""", (user_id,))
    teams = cursor.fetchall()

    workouts=[]
    # get recent workouts
    for team in teams:
        team_id=team[0]

        cursor.execute("""SELECT workout_id, date_assigned 
                      FROM Workout 
                      WHERE team_id=%s
                      ORDER BY date_assigned DESC
                      LIMIT 5""", 
                  (team_id,))
        workouts= cursor.fetchall()
    

    return render_template('athlete.html', 
                            user_id=user_id,
                            athlete=athlete, 
                            teams=teams, 
                            workouts=workouts)


# Endpoint for performance form submission
@program.route('/input/<int:workout_id>', methods=['POST'])
@login_required
def input(workout_id):
    cursor = g.db.cursor()
    user_id = session['user_id']
    cursor.execute('SELECT E.eid FROM consists_of E WHERE E.workout_id=%s',(workout_id,))
    eids = cursor.fetchall()
    # loops through form submission and inserts into performance table
    for eid in eids:
        reps=int(request.form['reps%s' % eid])
        weight=int(request.form['max%s' % eid])
        cursor.execute('INSERT INTO performance VALUES (%s, %s, %s, %s, %s)', (eid[0], user_id, workout_id, reps, weight))
    cursor.execute('INSERT INTO does VALUES (%s, %s, %s)', (workout_id,user_id,datetime.now()))
    g.db.commit()    
    return redirect(url_for('athlete_performance',user_id=user_id,workout_id=workout_id))

### General User Views ###

# Endpoint for login form submission
@program.route('/login', methods=['POST'])
def login():
    email_address = request.form['email_address'] 
    password = request.form['password']
    cursor = g.db.cursor()
    cursor.execute('SELECT user_id, name, password FROM User WHERE email_address = %s',
                   (email_address, ))
    # if one user was found, then this is that user
    if int(cursor.rowcount) == 1:
        user = cursor.fetchone()
        # we check the password against the hash stored in the db
        if check_password_hash(user[2], password):
            # fetch user_id
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            cursor.execute('SELECT pay FROM Coach WHERE user_id = %s', (user[0]))
            # if not a coach, then we have an athlete
            if int(cursor.rowcount == 0):
                session['user_type'] = 'athlete'
            else:
                session['user_type'] = 'coach'
            return redirect(url_for('index'))
    # either 0 or more than one (which really shouldn't hprogramen)
    flash('Your email_address and password wasn\'t found.', 'error')
    return redirect(url_for('index'))


# Registers a user
@program.route('/register', methods=['POST'])
def register():
    # Grab the information from the request body
    name = request.form['name']
    email_address = request.form['email_address']
    password = request.form['password']
    user_type = request.form['type'].lower()
    team_id = int(request.form['team'])
    cursor = g.db.cursor()
    # first check if user with email_address address already exists
    cursor.execute('SELECT * FROM User WHERE email_address = %s', (email_address,))
    # if any user was found, then cannot register with that email_address
    if int(cursor.rowcount) != 0:
        flash('That email_address address is already taken.', 'error')
        return redirect(url_for('index'))

    user_id = 0
    # if the user is an athlete, then we insert them into the Athletes table
    # and put them on a team, as well as insert them into the User table
    if user_type == 'athlete':
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        cursor.execute('INSERT INTO User(name, email_address, password) VALUES(%s, %s, %s)', 
                    (name, email_address, generate_password_hash(password)))
        user_id = cursor.lastroworkout_id
        cursor.execute('INSERT INTO Athlete VALUES(%s, %s, %s)',
                    (user_id, height, weight))
        cursor.execute('INSERT INTO member_of VALUES(%s, %s, "Bench", NextTeamNumber(%s))',
                        (user_id, team_id, team_id))
    # if the user is a coach, then we insert them into the Coach table
    # and have them coach a team, as well as insert them into the User table
    elif user_type == 'coach':
        pay = float(request.form['pay'])

        cursor.execute('INSERT INTO User(name, email_address, password) VALUES(%s, %s, %s)', 
                    (name, email_address, generate_password_hash(password)))
        user_id = cursor.lastroworkout_id
        cursor.execute('INSERT INTO Coach VALUES(%s, %s)', (user_id, pay))
        cursor.execute('INSERT INTO coaches VALUES(%s, %s, %s)',
                        (user_id, team_id, datetime.now()))
    # commit the transaction
    g.db.commit()

    # set the cookies
    session['user_id'] = user_id
    session['user_name'] = name
    session['user_type'] = user_type
    flash('You were successfully registered and logged in.', 'success')
    return redirect(url_for('index'))


# Logs a user out. We do this by deleting the session cookies that contain 
# currently logged in users information.
@program.route('/logout')
def logout():
    try:
        session.pop('user_id')
        session.pop('user_name')
        session.pop('user_type')
    except KeyError:
        pass
    finally:
        return redirect(url_for('index'))

# This function is run before every request. It connects to the database
# and stores the connection on the "g" object, which is available for
# the lifetime of a request.
@program.before_request
def before_request():
    g.db = mysql.connect(host = program.config['DB_HOST'], 
                         db = program.config['DB_NAME'],
                         user = program.config['DB_USER'],
                         passwd = program.config['DB_PASSWORD'])

# Closes the database connection after a request finishes
@program.teardown_request
def teardown_request(exception):
    g.db.close()


if __name__ == '__main__':
    program.run()
