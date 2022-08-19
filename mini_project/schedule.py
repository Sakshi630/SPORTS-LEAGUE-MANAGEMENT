import psycopg2

POSTGRESQL_URI="postgres://kxyxqccj:6hzGd6qlulzViWmhmfLxUUmzGgd7Hl25@john.db.elephantsql.com:5432/kxyxqccj"

connetion= psycopg2.connect(POSTGRESQL_URI)

cur= connetion.cursor()

sql = 'select name from account '

cur.execute(sql)

results = cur.fetchall()

teams=(results)
matches=[]
team1=0
while team1<len(teams):
    team2=team1+1    # start
    while team2<len(teams):
        matches.append((teams[team1],teams[team2]))
        team2+=1
    team1+=1
for i in matches: 
    print (i)


for i in matches: 
    try:
        with connetion:
            with connetion.cursor() as cursor:
                cursor.execute(
                "CREATE TABLE Schedule (Player1 TEXT,Player2 TEXT );"
                )
    except psycopg2.errors.DuplicateTable:
        pass

    with connetion:
        with connetion.cursor() as cursor:
            sql ='INSERT INTO Schedule (Player1 ,Player2) VALUES (%s, %s)'
            cursor = connetion.cursor()
            cursor.execute(sql, i)
            connetion.commit()

