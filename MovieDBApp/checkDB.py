from MovieDBApp.models import *
import psycopg2

# Establish a connection to the database
conn = psycopg2.connect(database='MovieDB', user='postgres', password='password', host='20.216.170.49', port='5432') 


def checkManagerCredentials(manager_name, pw): #check database manager's credentials from database
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.database_manager WHERE manager_username = '" +manager_name + "' AND password = '" + pw + "'" #check for directors
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    return(len(rows)==1)

def regulate_rows(row):
    name = ""
    str_row = str(row)
    for character in str_row: # instead of writing ('BollywoodIMDB       ',)  write BollywoodIMDB
        if character != " " and character != "," and character != "(" and character != ")" and character != "'":
            name += character
    return name

def getAllPlatformNames(): #get all platform names from database
    cur = conn.cursor()
    sql_query = "SELECT platform_name FROM public.platform ORDER BY platform_name ASC"
    cur.execute(sql_query)
    rows = cur.fetchall()
    my_rows = []
    for row in rows: # instead of writing ('BollywoodIMDB       ',) 
        my_rows.append(regulate_rows(row))
    cur.close()
    return my_rows

def uniqueUserName(username): #check whether director or audience has that username
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.director WHERE username = '" +username + "'" #check for directors
    cur.execute(sql_query)
    rows = cur.fetchall()
    total_len = 0
    total_len += len(rows) #if it finds something total length will greater than 0
    sql_query = "SELECT * FROM public.audience WHERE username = '" +username + "'"
    cur.execute(sql_query)
    rows = cur.fetchall()
    total_len += len(rows)
    cur.close()
    return(total_len==0)

def addDirector(name, surname, username, nation, password, platform_name): #add director to database
    cur = conn.cursor()
    if (platform_name == None): #if platform is not selected
        sql_query = "INSERT INTO public.director (name, surname, username, nation, password) VALUES (%s, %s, %s, %s, %s);"
        values = (name, surname, username, nation, password)
        cur.execute(sql_query, values)
        conn.commit()
        cur.close()
    else:
        sql_query = "SELECT platform_id From public.platform WHERE platform_name = '" + platform_name +"'"
        cur.execute(sql_query)
        rows = cur.fetchall()
        platform_id = int(regulate_rows(rows[0] )) #sth like (10130,) to 10130 as int
        sql_query = "INSERT INTO public.director (name, surname, username, nation, password, platform_id) VALUES (%s, %s, %s, %s, %s,%s);"
        values = (name, surname, username, nation, password,platform_id)
        cur.execute(sql_query, values)
        conn.commit()
        cur.close()

def addAudience(name, surname, username, password): #add audience to database
    cur = conn.cursor()
    sql_query = "INSERT INTO public.audience (name, surname, username, password) VALUES (%s, %s, %s, %s);"
    values = (name, surname, username, password)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def getAllDirectors(): #get all directors
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.director ORDER BY username ASC"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_directors = [] 
    for row in rows:
        lst = []
        for attributes in row:
            lst.append(regulate_rows(attributes))
        if (lst[5]=="None"): #if it's none as a string convert it back to the None again
            director = Director_class(lst[0],lst[1],lst[2],lst[3],lst[4],None)
            all_directors.append(director)
        else:
            director = Director_class(lst[0],lst[1],lst[2],lst[3],lst[4],lst[5])
            all_directors.append(director)
    cur.close()
    return all_directors

class Director_class: #this is for holding directors in a list (to show them in html, html couldn't get index of list)
  def __init__(self, name, surname, username, nation, password, platform_id):
    self.name = name
    self.surname = surname
    self.username = username
    self.nation = nation
    self.password = password
    self.platform_id = platform_id


def getAllAudiences(): #get all directors
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.audience ORDER BY username ASC"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_audiences = [] 
    for row in rows:
        lst = []
        for attributes in row:
            lst.append(regulate_rows(attributes))
        audience = Audience_class(lst[0],lst[1],lst[2])
        all_audiences.append(audience)

    cur.close()
    return all_audiences

class Audience_class: #this is for holding directors in a list (to show them in html, html couldn't get index of list)
  def __init__(self, name, surname, username):
    self.name = name
    self.surname = surname
    self.username = username

def update_platform(director_username, platform_id):
    cur = conn.cursor()
    sql_query = "UPDATE public.director SET platform_id = %s WHERE username = %s ;"
    values = (platform_id, director_username)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def checkDirectorUsername(username): #check whether director or audience has that username
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.director WHERE username = '" +username + "'" #check for directors
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    return (len(rows) == 1)

def checkPlatformID(platform_id): #check whether director or audience has that username
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.platform WHERE platform_id = '" +platform_id + "'" #check for directors
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    return (len(rows) == 1)

def deleteAudience(username):
    cur = conn.cursor()
    sql_query = "DELETE FROM public.audience WHERE username = '" +username+"';"
    cur.execute(sql_query)
    conn.commit()
    cur.close()
    
def checkAudienceUsername(username): #check whether director or audience has that username
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.audience WHERE username = '" +username + "'" #check for directors
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    return (len(rows) == 1)


def checkDirectorCredentials(username, pw): #check director's credentials from database
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.director WHERE username = '" +username + "' AND password = '" + pw + "'" 
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    return(len(rows)==1)


def addMovie(movie_id, movie_name, duration, director_name): #add audience to database
    cur = conn.cursor()
    sql_query = "INSERT INTO public.directed_movie (movie_id, movie_name, duration, username) VALUES (%s, %s, %s, %s);"
    values = (movie_id, movie_name, duration, director_name)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()