from termios import VSUSP
from django.urls import path
from .import views


urlpatterns = [
    path('', views.Home_Page, name = "home-page"),
    path('create_room/', views.create_room, name="create_room"),
    # path('room/<str:room_code>/', views.room, name="room"),
    path('room/<str:room_code>/<str:created>/', views.room, name="room"),
    path('joinroom/<str:room_code>/', views.joinRoom, name="join-room"),
    # path('joinroom/<str:room_code>/<str:created>/', views.room, name="join-room"),

    path('login/', views.login_page, name="login-page"),
    path('logout/', views.logout_page, name="logout-page"),
    path('register/', views.register_page, name="register-page"),
    path('change-password/', views.change_password, name="change-password"),


    path('uploadVideo/', views.uploadVideo, name = "uploadVideo"),

    path('video/<str:room_id>/', views.playVideo, name = "playVideo"),

    path('updateMesssage/', views.updateMessage, name = 'updateMessage'),
]