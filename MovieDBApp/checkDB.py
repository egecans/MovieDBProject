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

#
def addTheatre(district, theatre_name, capacity, theatre_id):
    cur = conn.cursor()
    sql_query = "INSERT INTO public.theatre (district, theatre_name, capacity, theatre_id) VALUES (%s, %s, %s, %s);"
    values = (district, theatre_name, capacity, theatre_id)
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

def checkAudienceCredentials(username, pw): #check director's credentials from database
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.audience WHERE username = '" +username + "' AND password = '" + pw + "'" 
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

def getListTheatres(given_slot): #list available theaters for given slot
    cur = conn.cursor()
    sql_query = "SELECT district, theatre_name, capacity, theatre_id FROM public.theatre WHERE theatre_id NOT IN(SELECT T.theatre_id FROM public.theatre T INNER JOIN public.located L ON T.theatre_id = L.theatre_id INNER JOIN public.movie_session S ON L.session_id = S.session_id WHERE S.time_slot ="+given_slot+");"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_theaters = [] 
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        theatre = Theatre_class(lst[0],lst[1],lst[2], lst[3])
        all_theaters.append(theatre)
    cur.close()
    return all_theaters

class Theatre_class: #this is for holding theatres in a list (to show them in html, html couldn't get index of list)
  def __init__(self, district, theatre_name, capacity, theatre_id):
    self.district = district
    self.theatre_name = theatre_name
    self.capacity = capacity
    self.theatre_id = theatre_id

def getMovieDuration(movie_id): # get duration of movie
    cur = conn.cursor()
    sql_query = "SELECT duration FROM public.directed_movie WHERE movie_id = " + str(movie_id)
    cur.execute(sql_query)
    rows = cur.fetchall()
    my_row = regulate_rows(rows)
    cur.close()
    return my_row[1]


#
def addMovieRelations(time_slot, date, movie_id, theatre_id): # if time credentials are ok (theatre is available for this movie) this func is insert movie session and corresponding relations play and located
    if (checkTimeOK(theatre_id,date,movie_id, time_slot)):
        session_id = str(movie_id) + str(theatre_id) + str(time_slot) #it must be unique!
        addMovieSession(session_id,date,time_slot)
        addPlay(session_id,movie_id)
        addLocated(session_id, theatre_id)
        return True
    else: #if it couldn't insert return Fase
        return False


def addMovieSession(session_id, date, time_slot): #add Movie Session to Database
    cur = conn.cursor()
    sql_query = "INSERT INTO public.movie_session (date, time_slot, session_id) VALUES (%s, %s, %s);"
    values = (date, time_slot, session_id)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def addPlay(session_id, movie_id): #add Play relation between Movie Session and Movie
    cur = conn.cursor()
    sql_query = "INSERT INTO public.play (session_id, movie_id) VALUES (%s, %s);"
    values = (session_id,movie_id)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def addLocated(session_id, theatre_id): #add Located relation between Movie Session and Theatre
    cur = conn.cursor()
    sql_query = "INSERT INTO public.located (session_id, theatre_id) VALUES (%s, %s);"
    values = (session_id,theatre_id)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

#theatre_id de lazım
#data de lazım
def checkTimeOK(theatre_id,date,movie_id, time_slot): #in this function it checks, whether duration of movie and time slot is ok for add the movie session. It needs to be <= 4
    movie_duration = getMovieDuration(movie_id)
    print("2")
    if (int(time_slot) + int(movie_duration) < 6): #if it is smaller than 6 in slot 4 duration 1 it's 5 because there are 1,2,3,4 slots in theatres.
        cur = conn.cursor()
        print("1")

        sql_query = "SELECT S.time_slot, MOV.duration from public.located L, public.movie_session S, public.directed_movie MOV, public.play PL WHERE L.theatre_id = %s and  L.session_id = S.session_id and  S.date = %s and PL.session_id = S.session_id and PL.movie_id = MOV.movie_id ;"
        #it returns not available slot and duration of movie on that slot, with these informations we calculate which slots are not ok.
        values = (theatre_id, date)
        cur.execute(sql_query, values)
        rows = cur.fetchall()
        print(rows)
        cur.close()
        if (rows == []): # if it is fully available
            return True
        
        available_slots = [1,2,3,4]
        for tuple in rows:
            not_ok_slots_until = tuple[0] + tuple[1] # i.e (1,2) 1+2 until 3 it's not available 
            for i in range(tuple[0],not_ok_slots_until): # in range [1,3) remove the values from range and the rest of them are available
                available_slots.remove(i)
        print(available_slots)
        if time_slot in available_slots:
            return True
        # locateddan theatre idsi girilince movie sessionlarına bak var mı diye çok şey var kolayla başla
        # playdan movie sessions'ın IDsiyle movie'sini bul
        # movie'nin durationını çek
        # x = movie session'ın time slotu çektim
        # y = time slot + durationı hesapla.
        # 1,4 araında x,y range'inde olmayan ne varsa availabledır.


#dene
def getSessionIDs(theatre_id):
    cur = conn.cursor()
    sql_query = "SELECT session_id FROM public.located WHERE theatre_id = " + str(theatre_id)
    cur.execute(sql_query)
    rows = cur.fetchall()
    my_rows = []
    for row in rows: # instead of writing ('BollywoodIMDB       ',) 
        my_rows.append(regulate_rows(row))
    cur.close()
    return my_rows

def addNextTo(pre, suc): #add predecessor to database
    cur = conn.cursor()
    sql_query = "INSERT INTO public.next_to (pre_id, suc_id) VALUES (%s, %s);"
    values = (pre, suc)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def getAllMovies():
    cur = conn.cursor()
    sql_query = "SELECT DM.movie_id, DM.movie_name, D.surname AS director_surname, P.platform_name AS platform, T.theatre_id, MS.time_slot, STRING_AGG(CAST(N.pre_id AS TEXT), ', ') AS predecessors_list FROM Directed_Movie DM INNER JOIN Director D ON DM.username = D.username INNER JOIN Platform P ON DM.avg_rating = P.platform_id INNER JOIN Play PY ON DM.movie_id = PY.movie_id INNER JOIN Movie_Session MS ON PY.session_id = MS.session_id INNER JOIN Located L ON MS.session_id = L.session_id INNER JOIN Theatre T ON L.theatre_id = T.theatre_id LEFT JOIN Next_To N ON DM.movie_id = N.suc_id GROUP BY DM.movie_id, DM.movie_name, D.surname, P.platform_name, T.theatre_id, MS.time_slot;"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_movies = [] 
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        movie = Movie_class(lst[0],lst[1],lst[2], lst[3], lst[4], lst[5])
        all_movies.append(movie)
    cur.close()
    return all_movies


class Movie_class: #this is for holding movies in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, surname, platform, theatre_id, time_slot, predecessors_list):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.surname = surname
    self.platform = platform
    self.theatre_id = theatre_id
    self.time_slot = time_slot
    self.predecessors_list = predecessors_list