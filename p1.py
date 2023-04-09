import json
import sqlite3

#PART 1: Creating the database
dbname = "roster.sqlite"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Course;
	DROP TABLE IF EXISTS Member;
	CREATE TABLE User (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE 
	);
	CREATE TABLE Course (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		title TEXT UNIQUE
	);
	CREATE TABLE Member (
		user_id INTEGER,
		course_id INTEGER,
		role INTEGER,
		PRIMARY KEY(user_id, course_id)
	)
''')


jsondata = open("roster_data.json")
data = json.load(jsondata)

#PART 3: INSERTING DATA
for entry in data:
	user = entry[0]
	course = entry[1]
	instructor = entry[2]

	#Inserting user
	user_statement = """INSERT OR IGNORE INTO User(name) VALUES( ? )"""
	SQLparams = (user, )
	cur.execute(user_statement, SQLparams)

	#Inserting course
	course_statement = """INSERT OR IGNORE INTO Course(title) VALUES( ? )"""
	SQLparams = (course, )
	cur.execute(course_statement, SQLparams)

	#Getting user and course id
	courseID_statement = """SELECT id FROM Course WHERE title = ?"""
	SQLparams = (course, )
	cur.execute(courseID_statement, SQLparams)
	courseID = cur.fetchone()[0]
     
	userID_statement = """SELECT id FROM User WHERE name = ?"""
	userName_statment="""SELECT name FROM User Where  id =?"""
    #fetch the  data 
	SQLparams = (user, )
	cur.execute(userID_statement, SQLparams)
	userID = cur.fetchone()[0]

	#Inserting the entry
	member_statement = """INSERT INTO Member(user_id, course_id, role)
		VALUES(?, ?, ?)"""
	SQLparams = (userID, courseID, instructor)
	cur.execute(member_statement, SQLparams)
	

#Saving the changes
conn.commit()

#PART 4: Testing and obtaining the results
test_statement = """
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;

"""
cur.execute(test_statement)
result = cur.fetchone()
print("The first row in the resulting record set: " + str(result))

#Closing the connection
cur.close()
conn.close()