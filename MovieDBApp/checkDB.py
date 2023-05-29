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


#session ID gircem
def checkUserCanBuy(username, session_id):
    cur = conn.cursor() #retrieve the movie sessions audience bought.
    sql_query = "SELECT session_id FROM public.buy WHERE username = '" + username +"';" #check the session's audience bought.
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    list_of_bought_sessions = []
    for row in rows:
        list_of_bought_sessions.append(regulate_rows(row))
    if (session_id in list_of_bought_sessions): #if user has already buy a ticket this session before
        print("ALINMIŞ")
        return False
    
    cur = conn.cursor() #retrieve the movies audience bought.
    sql_query = "SELECT Pl.movie_id FROM public.buy B , public.play Pl WHERE username = '" + username +"' and Pl.session_id = B.session_id;" 
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    list_of_bought_movies = []
    for row in rows:
        list_of_bought_movies.append(regulate_rows(row))


    cur = conn.cursor() #get predecessors of the movie in selected session
    sql_query = "SELECT pre_id FROM public.play Pl, public.next_to Nt WHERE Pl.session_id = " + session_id + " and Pl.movie_id = Nt.suc_id;" 
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    list_of_predecessors = []
    for row in rows:
        list_of_predecessors.append(regulate_rows(row))

    if (is_sublist(list_of_predecessors, list_of_bought_movies)): #if user buy tickets for all predecessors of the movie in the movie session
        print("PRELER İZLENMİŞ")
        cur = conn.cursor() #get the date of session
        sql_query = "SELECT date FROM public.movie_session WHERE session_id = " + session_id + ";" 
        cur.execute(sql_query)
        session_date = cur.fetchall()[0][0]
        print(session_date)
        #get movie id and date of all predecessors which watched by audience
        sql_query = "SELECT PlSuc.movie_id, Ms.date FROM public.play PlSuc, public.movie_session Ms, public.Buy B WHERE PlSuc.session_id = Ms.session_id and B.username = %s and B.session_id = Ms.session_id and PlSuc.movie_id IN (SELECT pre_id FROM public.play Pl, public.next_to Nt WHERE Pl.session_id = %s and Pl.movie_id = Nt.suc_id);"
        values = (username, session_id)
        cur.execute(sql_query,values)
        bought_pre_dates = cur.fetchall()
        cur.close()
        print(bought_pre_dates)
        min_dates_dict = {}
        for rows in bought_pre_dates:
            current_movie_id = rows[0]
            current_session_date = rows[1]
            if current_movie_id  in min_dates_dict: #if user watch predecessor movie more than 1 time
                if min_dates_dict.get(current_movie_id) > current_session_date: #if existed date is bigger than current one change its date
                    min_dates_dict[current_movie_id] = current_session_date 
            else: #if it is not in the dictionary insert it
                min_dates_dict[current_movie_id] = current_session_date

        values_list = list(min_dates_dict.values()) #convert it to list
        for date in values_list: #dates are predecessor dates of the current movie of the session
            if date > session_date: #if any predecessor's min date is bigger than current session return false
                return False
        
        return True
    else:
        return False

def capacity_ok(session_id): #check if capacity is ok
    cur = conn.cursor() #get the date of session
    sql_query = "SELECT CASE WHEN ((SELECT Th.capacity FROM public.theatre Th, public.located WHERE located.session_id = %s and located.theatre_id = Th.theatre_id) > (SELECT COUNT(*) FROM public.buy WHERE session_id = %s)) THEN 'TRUE' ELSE 'FALSE' END AS can_buy;" 
    cur.execute(sql_query,(session_id,session_id))
    result = cur.fetchone()[0]
    cur.close()
    print(result)
    if result == "TRUE":
        return True
    return False


def is_sublist(sub, main):
    set1 = set(sub)
    set2 = set(main)
    return set1.issubset(set2)

def buySession(username, session_id):
    if (checkUserCanBuy(username, session_id) and capacity_ok(session_id)): #if user can buy a session with given constraints
        cur = conn.cursor()
        sql_query = "INSERT INTO public.buy (username, session_id) VALUES (%s, %s);"
        values = (username, session_id)
        print(values)
        cur.execute(sql_query, values)
        conn.commit()
        cur.close()
        return True
    else:
        return False
    
    

def update_movie(movie_name, movie_id):
    cur = conn.cursor()
    sql_query = "UPDATE public.directed_movie SET movie_name = %s WHERE movie_id = %s ;"
    values = (movie_name, movie_id)
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

def checkMovieID(movie_id): 
    cur = conn.cursor()
    sql_query = "SELECT * FROM public.directed_movie WHERE movie_id = '" +movie_id + "'"
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


def addMovie(movie_id, movie_name, duration, director_name):
    cur = conn.cursor()
    sql_query = "INSERT INTO public.directed_movie (movie_id, movie_name, duration, username) VALUES (%s, %s, %s, %s);"
    values = (movie_id, movie_name, duration, director_name)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def getRating(username):
    cur = conn.cursor()
    sql_query = "SELECT dm.movie_id, dm.movie_name, r.rating FROM public.directed_movie dm INNER JOIN public.rate r ON dm.movie_id = r.movie_id WHERE r.username = '"+username+"';"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_ratings = [] 
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        rating = Rating_class(lst[0],lst[1],lst[2])
        all_ratings.append(rating)
    cur.close()
    return all_ratings

class Rating_class: #this is for holding theatres in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, rating):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.rating = rating

def getDirectorMovie(username):
    cur = conn.cursor()
    sql_query = "SELECT dm.movie_id, dm.movie_name, l.theatre_id, t.district, ms.time_slot FROM public.directed_movie dm INNER JOIN public.play p ON dm.movie_id = p.movie_id INNER JOIN public.movie_session ms ON p.session_id = ms.session_id INNER JOIN public.located l ON ms.session_id = l.session_id INNER JOIN public.theatre t ON l.theatre_id = t.theatre_id WHERE dm.username = '"+username+"';"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_movies = [] 
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        movie = DirectorMovie_class(lst[0],lst[1],lst[2],lst[3],lst[4])
        all_movies.append(movie)
    cur.close()
    return all_movies

class DirectorMovie_class: #this is for holding theatres in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, theatre_id, district, time_slot):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.theatre_id = theatre_id
    self.district = district
    self.time_slot = time_slot

def getAvgRating(movie_id):
    cur = conn.cursor()
    sql_query = "SELECT dm.movie_id, dm.movie_name, AVG(r.rating) AS overall_rating FROM public.directed_movie dm INNER JOIN public.rate r ON dm.movie_id = r.movie_id WHERE dm.movie_id = '"+movie_id+"' GROUP BY dm.movie_id, dm.movie_name;"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_ratings = [] 
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        rating = AvgRating_class(lst[0],lst[1],lst[2])
        all_ratings.append(rating)
    cur.close()
    return all_ratings

class AvgRating_class: #this is for holding theatres in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, avg_rating):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.avg_rating = avg_rating

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
        return False
    else:
        return False

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

def getMyMovieSessions(username):
    cur = conn.cursor()
    sql_query = "SELECT DM.movie_id, DM.movie_name, B.session_id, R.rating, avg_rating.avg_rating FROM public.buy B JOIN public.play Pl ON B.session_id = Pl.session_id JOIN public.directed_movie DM ON Pl.movie_id = DM.movie_id LEFT JOIN public.rate R ON R.username = %s AND R.movie_id = DM.movie_id LEFT JOIN (SELECT movie_id, SUM(rating)/COUNT(*) AS avg_rating FROM public.rate WHERE rating IS NOT NULL GROUP BY movie_id) AS avg_rating ON avg_rating.movie_id = DM.movie_id WHERE B.username = %s;"    
    cur.execute(sql_query,(username,username))
    rows = cur.fetchall()
    cur.close()
    my_sessions=[]
    for tuple in rows:
        my_sessions.append(MySessions_class(tuple[0],regulate_rows(tuple[1]),tuple[2],tuple[3],tuple[4]))
    return my_sessions

class MySessions_class: #this is for holding movies in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, session_id, rating, avg_rating):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.session_id = session_id
    self.rating = rating
    self.avg_rating = avg_rating


def addNextTo(pre, suc): #add predecessor to database
    cur = conn.cursor()
    sql_query = "INSERT INTO public.next_to (pre_id, suc_id) VALUES (%s, %s);"
    values = (pre, suc)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()

def getAllMovies():
    cur = conn.cursor()
    sql_query = "SELECT DM.movie_id, DM.movie_name, D.surname AS director_surname, AG.platform_id AS platform, L.theatre_id, MS.time_slot, STRING_AGG(CAST(N.pre_id AS TEXT), ', ') AS predecessors_list FROM public.directed_movie AS DM INNER JOIN public.director D ON DM.username = D.username INNER JOIN public.play P ON DM.movie_id = P.movie_id INNER JOIN public.movie_session MS ON P.session_id = MS.session_id INNER JOIN public.located L ON MS.session_id = L.session_id LEFT JOIN public.agreement AG ON AG.username = D.username LEFT JOIN public.next_to N ON DM.movie_id = N.suc_id GROUP BY DM.movie_id, D.surname, AG.platform_id, L.theatre_id, MS.time_slot;"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_movies = []
    for row in rows:
        lst=[]
        for i in range(0,7):
            if ( i != 6): # if it is not predecessor list
                lst.append(regulate_rows(row[i]))
            else:
                lst.append(row[i])
        movie = Movie_class(lst[0],lst[1],lst[2],lst[3], lst[4], lst[5], lst[6])
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

def getMyMovies(director_name):
    cur = conn.cursor()
    sql_query = "SELECT dm.movie_id, dm.movie_name, l.theatre_id, ms.time_slot, (SELECT STRING_AGG(CAST(N.pre_id AS VARCHAR), ', ') FROM public.next_to N WHERE N.suc_id = dm.movie_id) AS predecessors_list FROM public.directed_movie dm INNER JOIN public.play p ON dm.movie_id = p.movie_id INNER JOIN public.movie_session ms ON p.session_id = ms.session_id INNER JOIN public.located l ON ms.session_id = l.session_id WHERE dm.username = '"+director_name+"' ORDER BY dm.movie_id ASC;"
    cur.execute(sql_query)
    rows = cur.fetchall()
    all_movies = []
    for row in rows:
        lst=[]
        for i in range(0,5):
            if ( i != 4): # if it is not predecessor list
                lst.append(regulate_rows(row[i]))
            else:
                lst.append(row[i])
        movie = myMovie_class(lst[0],lst[1],lst[2],lst[3], lst[4])
        all_movies.append(movie)
    cur.close()
    return all_movies

class myMovie_class: #this is for holding movies in a list (to show them in html, html couldn't get index of list)
  def __init__(self, movie_id, movie_name, theatre_id, time_slot, predecessors_list):
    self.movie_id = movie_id
    self.movie_name = movie_name
    self.theatre_id = theatre_id
    self.time_slot = time_slot
    self.predecessors_list = predecessors_list


def getAudsWhoBought(given_movie_id): #list auds who bouht ticket for a specified film
    cur = conn.cursor()
    sql_query = "SELECT a.username, a.name, a.surname FROM public.audience a INNER JOIN public.buy b ON a.username = b.username INNER JOIN public.play p ON b.session_id = p.session_id INNER JOIN public.directed_movie dm ON p.movie_id = dm.movie_id WHERE dm.movie_id = "+given_movie_id+";"
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    all_auds = []
    for row in rows:
        print(row)
        lst=[]
        for attributes in row:
            lst.append(regulate_rows(attributes))
        aud = Audience_class(lst[0],lst[1],lst[2])
        all_auds.append(aud)
    return all_auds

class Audience_class: #this is for holding movies in a list (to show them in html, html couldn't get index of list)
  def __init__(self, username, name, surname):
    self.username = username
    self.name = name
    self.surname = surname

def getMoviedIDs(audience_name):
    cur = conn.cursor()
    sql_query = "SELECT Pl.movie_id FROM public.buy B, public.play Pl WHERE B.username = '" + audience_name+ "' and B.session_id = Pl.session_id"
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    id_list = []
    for row in rows:
        id_list.append(row[0])
    return id_list

def addRate(audience_name, movie_id, rate):
    cur = conn.cursor()
    sql_query = "INSERT INTO public.rate (username, movie_id, rating) VALUES (%s, %s, %s);"
    values = (audience_name, movie_id, rate)
    cur.execute(sql_query, values)
    conn.commit()
    cur.close()