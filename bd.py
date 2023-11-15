import sqlite3
connect = sqlite3.connect(r"bd.db", check_same_thread=False)
cursor = connect.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)''')
connect.commit()

cursor.execute(''' CREATE TABLE IF NOT EXISTS "accesses" (
	"id"	INTEGER NOT NULL,
	"level"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)''')
connect.commit()

links = ["Публичные", "Общего доступа", "Приватные"]
i=0
res=cursor.execute('''SELECT * FROM accesses''').fetchall()
if (len(res)==0):
	while i<len(links):
		cursor.execute('''INSERT INTO "accesses"(level) VALUES (?)''', [links[i]])
		connect.commit()
		i=i+1


cursor.execute('''CREATE TABLE IF NOT EXISTS "links" (
	"id"	INTEGER NOT NULL,
	"long"	TEXT NOT NULL,
	"short"	TEXT NOT NULL,
	"accesses_id"	INTEGER NOT NULL,
	"count"	INTEGER NOT NULL,
	"owner"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("accesses_id") REFERENCES "accesses"("id"),
	FOREIGN KEY("owner") REFERENCES "users"("id")
) ''')
connect.commit()

def registration(con,cur, login, password):
	cur.execute('''INSERT INTO "users"(login, password) VALUES(?,?)''', (login, password))
	con.commit()

def findUser(cur, login):
	log = cur.execute('''SELECT * FROM "users" WHERE login = ? ''', (login, )).fetchone()
	return log
def findAccesses(cur):
	return cur.execute('''SELECT * FROM "accesses"''').fetchall()

