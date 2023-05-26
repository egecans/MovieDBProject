from multiprocessing import context
import re
from tokenize import Name
from django.contrib.auth.forms import UserCreationForm
from turtle import isvisible
from unicodedata import name
from django.shortcuts import get_object_or_404, redirect, render #biz olusturduk
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory  #inline formset için 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from MovieDBApp.checkDB import *
from MovieDBApp.forms import *
from django.urls import reverse



# Create your views here.
def main(request):
    main_text = "view.main function is called"
    context = {'main_text': main_text}
    return render(request, 'main.html', context) #views


def loginDBManager(request):
    if request.method == "POST": #burada fronttan backe geri dönüyor
        manager_name = request.POST.get('username')
        password = request.POST.get('password')
        checkCredentials = checkManagerCredentials(manager_name, password) #it checks whether credentials are correct in db
        if (checkCredentials):
            return redirect('MovieDBApp:homeManager')
        else:
            messages.info(request, 'username or password is incorrect!')
    context={}
    return render(request,'manager_login.html',context) #html dosyası ismi

def homeDBManager(request):
    all_directors_list = getAllDirectors()
    all_audiences_list = getAllAudiences()
    checkTimeOK(40001,'2023-05-25',2, 4)
    context={'directors':all_directors_list, 'audiences':all_audiences_list}
    return render(request,'manager_home.html',context)

def createDirector(request):
    if request.method == "POST": #if method is POST (when form clicked Create button form is returned as POST) this is the communication btw frontend and this method
        form_name = request.POST.get('name') #get attributes from frontend
        form_surname = request.POST.get('surname')
        form_username = request.POST.get('username')
        form_nation = request.POST.get('nation')
        form_password  = request.POST.get('password')
        form_platform_name = request.POST.get('platform_name')
        #if attributes isn't blank (except platform) and has a unique username
        if (form_name != "" and form_surname != "" and form_username != "" and form_nation != "" and form_password != "" and uniqueUserName(form_name)):
            addDirector(name=form_name, surname = form_surname , username = form_username, nation = form_nation, password = form_password , platform_name = form_platform_name) #create a director in db
            return redirect('/manager_home/') #return to manager's home
        else:
            messages.info(request, 'You must enter all credentials except platform name and your username must be unique!')
        
    platform_names = getAllPlatformNames()
    context = {'names':platform_names}
    return render(request,'create_director.html',context)

def createAudience(request):
    if request.method == "POST": #if method is POST (when form clicked Create button form is returned as POST) this is the communication btw frontend and this method
        form_name = request.POST.get('name') #get attributes from frontend
        form_surname = request.POST.get('surname')
        form_username = request.POST.get('username')
        form_password  = request.POST.get('password')
        #if attributes isn't blank (except platform) and has a unique username
        if (form_name != "" and form_surname != "" and form_username != "" and form_password != "" and uniqueUserName(form_name)):
            addAudience(name=form_name, surname = form_surname , username = form_username, password = form_password) #create a audience in db
            return redirect('/manager_home/') #return to manager's home
        else:
            messages.info(request, 'You must enter all credentials and your username must be unique!')

    context = {}
    return render(request,'create_audience.html',context)

#
#addTheatre(district, theatre_name, capacity, theatre_id)
def createTheatre(request):
    if request.method == "POST": #if method is POST (when form clicked Create button form is returned as POST) this is the communication btw frontend and this method
        theatre_id = request.POST.get('theatre_id') #get attributes from frontend
        theatre_name = request.POST.get('theatre_name')
        district = request.POST.get('district')
        capacity  = request.POST.get('capacity')
        #if attributes isn't blank (except platform) and has a unique username
        if (theatre_id != "" and capacity != "" and theatre_name != "" and district != ""):
            addTheatre(district, theatre_name, capacity, theatre_id)
            return redirect('/manager_home/') #return to manager's home
        else:
            messages.info(request, 'You must enter all credentials!')

    context = {}
    return render(request,'create_theatre.html',context)

def updatePlatform (request):
    if request.method == "POST":
        director_username = request.POST.get('director_username')
        platform_id = request.POST.get('platform_id')
        if (director_username != "" and platform_id != ""):
            if (checkDirectorUsername(director_username) and checkPlatformID(platform_id)):
                update_platform(director_username,platform_id)
                return redirect('/manager_home/')
            else:
                messages.info(request, 'Director username or platform id is incorrect!')
        else:
            messages.info(request, 'You must enter all credentials!')
    context = {}
    return render(request,'update_platform.html',context)

def removeAudience (request):
    if request.method == "POST":
        audience_username = request.POST.get('audience_username')
        if (checkAudienceUsername(audience_username)):
            deleteAudience(audience_username)
            return redirect('/manager_home/')
        else:
            messages.info(request, 'Entered username is not in our system ')
    context = {}
    return render(request,'delete_audience.html',context)



def loginDirector(request):
    if request.method == "POST": #burada fronttan backe geri dönüyor
        director_name = request.POST.get('username')
        password = request.POST.get('password')
        checkCredentials = checkDirectorCredentials(director_name, password) #it checks whether credentials are correct in db
        if (checkCredentials):
            request.session['username'] = director_name #in this way data is stored you can get value with  request.session.get('username') function
            return redirect('/directorHome')
        else:
            messages.info(request, 'username or password is incorrect!')
    context={}
    return render(request,'director_login.html',context) #html dosyası ismi

def homeDirector(request):
    director_name = request.session.get('username')
    context={'username':director_name}
    return render(request,'director_home.html',context)

def createMovie(request,director_name): # has a dynamic url because we need to pass data from html, so we couldn't use request.session method 
    if request.method == "POST": #if method is POST (when form clicked Create button form is returned as POST) this is the communication btw frontend and this method
        movie_id = request.POST.get('movie_id') #get attributes from frontend
        movie_name = request.POST.get('movie_name')
        duration = request.POST.get('duration')
        #if attributes isn't blank (except platform) and has a unique username
        if (movie_id.isdigit() and duration.isdigit()): #check ID and duration is digit
            int_duration = int(duration)
            if (int_duration > 0 and int_duration < 5): #check duration is in range [1,4]
                addMovie(movie_id,movie_name,duration,director_name)
                request.session['username'] = director_name
                return redirect('/directorHome')
            else:
              messages.info(request, 'Duration must be integer and in range [1,4] and !')  
        else:
            messages.info(request, 'Duration and Movie ID must be integer !')

    context={'username':director_name}
    return render(request,'create_movie.html',context)

def createMovieSession(request):  
    if request.method == "POST":
        movie_id = request.POST.get('movie_id') #get attributes from frontend
        time_slot = request.POST.get('time_slot')
        date = request.POST.get('date')
        theatre_id = request.POST.get('theatre_id')
        print(movie_id, time_slot, date, theatre_id)
        if (movie_id.isdigit() and time_slot.isdigit() and theatre_id.isdigit()): #check ID and duration is digit
            int_time_slot = int(time_slot)
            if (int_time_slot > 0 and int_time_slot < 5): #check duration is in range [1,4]
                if (addMovieRelations(time_slot, date, movie_id, theatre_id)):
                    return redirect('/directorHome')
                else:
                   messages.info(request, 'Your entered credentials not OK, (Duration + time slot <= 5) or given theatre is not available in this slot') 
                
            else:
              messages.info(request, 'Time slot only can be 1,2,3 or 4 !')  
        else:
            messages.info(request, 'Movie ID and Time Slot and Theatre ID must be integer !')

    context={}
    return render(request,'create_movie_session.html',context)



def listTheatres(request):
    all_theatres_list = getListTheatres()
    context = {'theatres':[]}
    if request.method == 'POST': # if click button
        context={'theatres':all_theatres_list}
    return render(request,'list_theatre.html',context)

