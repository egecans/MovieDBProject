from django.urls import path
from . import views

#bir appteysen appin adını giriyorsun, eğer ana appin altında bir appse de her hrefte önce app adı : <url name> kullanıyorsun
app_name = 'MovieDBApp'

#viewsta yazdığın fonksiyonlar için url düzenliyorsun
#sayfaya gidip bu fonksiyonları kullandığında pathin ilk parametresine gönderiyor bulunduğun adresten
#eğer herkes için aynıysa normal url yapıyorsun ama objeden objeye değişiyorsa /<int <views parametre adı> > yapıp dynamic url oluşturuyorsun
#3. parametre ise hrefte çağırdığında url pathini yazma diye unique bir isim koyuyorsun, htmlde hrefte {% %} arasına o isimle çağırabiliyorsun
#ve bu sayede dynamicleşiyor, bir şeyleri değiştirsen de url kısmında ismi aynı olduğundan her kullandığın templeteı da değiştirmene gerek kalmıyor
urlpatterns = [
    path('loginManager/',views.loginDBManager,name='loginManager'),
    path('manager_home/',views.homeDBManager,name='homeManager'),
    

    path('', views.main, name='main'),

    path('createAudience/', views.createAudience, name='createAudience'),
    path('createDirector',views.createDirector,name='createDirector'),
    path('deleteAudience/', views.removeAudience, name='deleteAudience'),
    path('updateplatform/', views.updatePlatform, name='updatePlatform'),
    path('createTheatre/',views.createTheatre, name='createTheatre'),

    path('loginDirector/',views.loginDirector,name='loginDirector'),
    path('directorHome/', views.homeDirector, name='homeDirector'),
    path('createMovie/<str:director_name>/', views.createMovie, name='createMovie'), #dynamic url, has a parameter director_name which pass as a parameter to its method createMovie
    path('listTheatres/', views.listTheatres, name='listTheatres'),
    path('createMovieSession/',views.createMovieSession,name='createMovieSession'),
]