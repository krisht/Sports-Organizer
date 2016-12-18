DROP DATABASE IF EXISTS MyCoachDatabaseBig;

CREATE DATABASE MyCoachDatabaseBig;

GRANT ALL PRIVILEGES ON MyCoachDatabaseBig.* to admin@localhost IDENTIFIED BY 'admin';

USE MyCoachDatabaseBig;

CREATE TABLE `User` (
    uid INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(128),
    email VARCHAR(128) UNIQUE,
    password VARCHAR(54),
    isAdmin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (uid)
);

CREATE TABLE `Coach` (
    uid INTEGER NOT NULL,
    salary DOUBLE,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES User (uid)
        ON DELETE CASCADE
);

CREATE TABLE `Athlete` (
    uid INTEGER NOT NULL,
    height DOUBLE,
    weight DOUBLE,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES User (uid)
        ON DELETE CASCADE
);

CREATE TABLE `TeamMascot` (
    school VARCHAR(128),
    mascot VARCHAR(128),
    PRIMARY KEY (school)
);

CREATE TABLE `Team` (
    tid INTEGER NOT NULL AUTO_INCREMENT,
    school VARCHAR(128) NOT NULL,
    hometown VARCHAR(128),
    PRIMARY KEY (tid),
    FOREIGN KEY (school) REFERENCES TeamMascot (school)
        ON DELETE NO ACTION
);

CREATE TABLE `SportSeason` (
    name VARCHAR(64),
    season VARCHAR(6),
    PRIMARY KEY (name)
);

CREATE TABLE `Sport` (
    sid INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(64),
    PRIMARY KEY (sid),
    FOREIGN KEY (name) REFERENCES SportSeason (name)
        ON DELETE NO ACTION
);

CREATE TABLE `Workout` (
    wid INTEGER AUTO_INCREMENT NOT NULL,
    tid INTEGER NOT NULL,
    date_assigned DATETIME,
    uid INTEGER NOT NULL,
    PRIMARY KEY (wid),
    FOREIGN KEY (tid) REFERENCES Team (tid)
        ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES Coach (uid)
        ON DELETE CASCADE
);

CREATE TABLE `ExerciseMuscles` (
    name VARCHAR(128),
    muscle_group VARCHAR(32),
    PRIMARY KEY (name)
);

CREATE TABLE `Exercise` (
    eid INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(128) UNIQUE NOT NULL,
    PRIMARY KEY (eid),
    FOREIGN KEY (name) REFERENCES ExerciseMuscles (name)
        ON DELETE CASCADE
);

CREATE TABLE `coaches` (
    uid INTEGER NOT NULL,
    tid INTEGER NOT NULL,
    since DATE,
    PRIMARY KEY (uid, tid),
    FOREIGN KEY (uid) REFERENCES Coach (uid)
        ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES Team (tid)
        ON DELETE CASCADE
);

CREATE TABLE `plays` (
    sid INTEGER NOT NULL,
    tid INTEGER NOT NULL,
    PRIMARY KEY (sid, tid),
    FOREIGN KEY (sid) REFERENCES Sport (sid)
        ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES Team (tid)
        ON DELETE CASCADE
);

CREATE TABLE `member_of` (
    uid INTEGER NOT NULL,
    tid INTEGER NOT NULL,
    position VARCHAR(10),
    number INTEGER,
    PRIMARY KEY (uid, tid),
    FOREIGN KEY (uid) REFERENCES Athlete (uid)
        ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES Team (tid)
        ON DELETE CASCADE
);

CREATE TABLE `consists_of` (
    wid INTEGER,
    eid INTEGER NOT NULL,
    sets INTEGER,
    reps INTEGER,
    PRIMARY KEY (wid, eid),
    FOREIGN KEY (wid) REFERENCES Workout (wid)
        ON DELETE CASCADE,
    FOREIGN KEY (eid) REFERENCES Exercise (eid)
        ON DELETE CASCADE
); 

CREATE TABLE `does` (
    wid INTEGER,
    uid INTEGER,
    date_done DATETIME,
    PRIMARY KEY (wid, uid),
    FOREIGN KEY (wid) REFERENCES Workout (wid)
        ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES Athlete (uid)
        ON DELETE CASCADE
); 


CREATE TABLE `performance` (
    eid INTEGER,
    uid INTEGER,
    wid INTEGER,
    reps_performed INTEGER,
    max_weight DOUBLE,
    PRIMARY KEY (eid, uid, wid),
    FOREIGN KEY (wid) REFERENCES Workout (wid)
        ON DELETE CASCADE,
    FOREIGN KEY (eid) REFERENCES Exercise (eid)
        ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES Athlete (uid)
        ON DELETE CASCADE
); 

DELIMITER |
CREATE PROCEDURE TeamProgress (
    IN tid INTEGER,
    IN wid INTEGER
)
BEGIN
    (SELECT M.uid, A.name, FALSE as completed
    FROM member_of M, User A
    WHERE M.tid = tid 
        AND M.uid = A.uid
        AND M.uid NOT IN (SELECT D.uid FROM does D WHERE D.wid=wid)
    )
    UNION
    (SELECT M.uid, A.name, TRUE as completed
    FROM member_of M, User A
    WHERE M.tid = tid 
        AND M.uid = A.uid
        AND M.uid IN (SELECT D.uid FROM does D WHERE D.wid=wid)
    );
END |
DELIMITER ; 

DELIMITER $$
CREATE FUNCTION `NextTeamNumber` (tid INTEGER) RETURNS INTEGER
BEGIN
    DECLARE last INTEGER;
    SELECT MAX(number) INTO last FROM member_of WHERE tid=tid;
    RETURN last+1;
END $$
DELIMITER ; 