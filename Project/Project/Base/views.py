from email import message
import imp
from multiprocessing import context
from .forms import CustomRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import json
from .models import *
from .serializers import *
from django.db.models import Q
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .decorators import unauthenicated_user


@unauthenicated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            print("unidentified user")

        user = authenticate(request, username = username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            print("invalid username and password")

    return render(request, 'sign-in.html')



@unauthenicated_user
def register_page(request):
    forms = CustomRegistrationForm()

    if request.method ==  'POST':
        
        forms = CustomRegistrationForm(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('login-page')
        else:
            print("not okay")


    context = {
        'forms': forms
    }
    return render(request, 'register.html', context)


def logout_page(request):
    print("hello")
    logout(request)
    return redirect('home-page')


@login_required(login_url='/login/')
def change_password(request):
    forms = UserPasswordChangeForm(request.user)

    if request.method == 'POST':
        forms = UserPasswordChangeForm(request.user, request.POST)
        
        if forms.is_valid():
            forms.save()
            return redirect('login-page')

    return render(request, 'change_password.html', {'forms': forms})


@login_required(login_url='/login/')
# @unauthenicated_user
def Home_Page(request):
    q = request.GET.get('q')
    print(q)
    if q == None:
        q = ''
    
    topics = Topic.objects.all()

    # room = Video.room_set.all()

    # rooms = Room.objects.filter(
    #     Q(topic__name__icontains = q)|
    #     Q(name__icontains = q)|
    #     Q(description__icontains = q)
    # )

    rooms = Video.objects.filter(
         Q(room_id__topic__name__icontains = q)|
        Q(room_id__name__icontains = q)|
        Q(room_id__description__icontains = q)
    )

    liveRoom = Room.objects.filter(isLive=True)

    print(liveRoom)
    # roomser =RoomSerializer(rooms, many=True)
    # print(roomser.data)


    context = {
        'rooms': rooms,
        'topics': topics,
        'liveRoom': liveRoom,
        # 'ser':roomser.data
    }
    return render(request, 'home-page.html', context)


# @login_required(login_url='/login/')
def create_room(request):
    topics = Topic.objects.all()

    if request.method == 'POST':
        room_name = request.POST['room_name']
        topics_name = request.POST['topics_name']
        description = request.POST['description']

        topic, created = Topic.objects.get_or_create(name=topics_name)
        
        room = Room.objects.create(
            host = request.user,
            topic  = topic,
            name = room_name,
            description = description,
            isLive = True,
        )

        room.save()
        # print(room.room_code)
        return redirect(f'/room/{room.room_code}/created')

    context = {
        'topics': topics
    }
    return render(request, 'create_room.html', context)


@login_required(login_url='/login/')
def joinRoom(request, room_code):
    print("room", room_code)
    room = Room.objects.filter(room_code = room_code)

    if room:
        return redirect(f'/room/{room_code}/join/')
    else:
        return HttpResponse('no room')

    # return render(request, 'room.html')



@login_required(login_url='/login/')
def room(request, room_code, created):
    room = Room.objects.get(room_code = room_code)
    messages = Message.objects.filter(room = room)

    # if request.method == 'POST':
    #     message = request.POST.get('message')

    #     Message.objects.create(
    #         user = request.user,
    #         room = room,
    #         body = message
    #     )



    context = {
        'created': created,
        'room_code': room_code,
        'room': room,
        'messages': messages,        
        }
    return render(request, 'room.html', context)


@csrf_exempt
@login_required(login_url='/login/')
def uploadVideo(request):
    file = request.FILES.get("video")
    room_id = request.POST.get('room_id')
    
    room = Room.objects.get(id = room_id)

    room.isLive = False
    room.save()

    Video.objects.create(
        room_id = room,
        video = file
        
        )
    
    return JsonResponse("item added", safe=False)




@login_required(login_url='/login/')
def playVideo(request, room_id):
    print(room_id)
    room = Room.objects.get(id = room_id)
    
    video = room.video_set.all()
    
    context = {
        'video':video 
    }

    return render(request, 'video.html', context)


@csrf_exempt
def updateMessage(request):
    data = json.loads(request.body)
    message = data['message']
    room_code = data['room_code']
    
    room = Room.objects.get(room_code = room_code)
    
    message = Message.objects.create(
        user = request.user,
        room = room,
        body = message
    )

    return JsonResponse('message was sent', safe=False)