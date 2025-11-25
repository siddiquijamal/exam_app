from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage),
    path('showform/',views.showForm),
    path('viewquestions/',views.viewquestions),
    path('addquestions/',views.addquestions),
    path('updatequestion/',views.updatequestion),
    path('deletequestion/',views.deletequestion),
    path('registertionform/',views.registerationform,name = "register"),
    path('registeration/',views.registeration),
    path('loginform/',views.loginform,name = "login"),
    path('login/',views.login),
    path('nextquestion/',views.nextQuestion),
    path('previousquestion/',views.previousQuestion),
    path('startTest/',views.startTest),
    path('endexam/',views.endExam),
    path('senddata/',views.sendData),
    path('getuser/<str:uname>',views.getUser),
    path('getuserdetails/<uname>',views.getUserDetails),
    path('adduser/',views.addUser),
    path('updateuser/',views.updateUSer),
    path('deleteuser/<str:uname>/',views.deleteUser),
    path('getalluser/',views.getAllUser),
     path('getuserdetails2/<str:uname>/',views.getUserDetails2),
    
]