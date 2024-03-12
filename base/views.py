from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
import string



@csrf_exempt
def generate_password(request):
    if request.method == 'POST':
        length = int(request.POST.get('length', 5))  # You may adjust the default length as per your needs
        characters = string.ascii_uppercase + string.digits 
        generated_password = ''.join(random.choice(characters) for _ in range(length))
       
        return JsonResponse({'Room name':generated_password})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)



def getToken(request):
    appId = '79e8c96d627f45e98cfd3ca0d52090c4'
    appCertificate = '89e8891582ba45d09d064e2d5066ace5'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationalTimeInSeconds = 3600*24
    currentTimeStamp = time.time()
    privilegeExpiredTs =currentTimeStamp + expirationalTimeInSeconds
    role = 1


    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return  JsonResponse({'token':token,'uid':uid},safe=False)

def lobby(request):
    return render(request,'base/lobby.html')



def room(request):
    return render(request,'base/room.html')

@csrf_exempt

def createMember(request):
    data = json.loads(request.body)
    member, created =RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name':data['name']},safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid =uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)



@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member =RoomMember.objects.get(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted',safe=False)