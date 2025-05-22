from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken
import whisper
from summariser.views import summaryFunction


ph = argon2.PasswordHasher()
model = whisper.load_model("base")

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
def createAccount(request):
    user_fname = request.data.get('fname')
    user_lname = request.data.get('lname')
    user_email = request.data.get('email')
    user_password = request.data.get('password')
    print(user_fname, user_lname, user_email)
    
    hash = ph.hash(user_password)
    print(hash)

    try:
        userExist = Users.objects.get(email=user_email)
        return Response(status=409)
    except:
        user = Users(first_name=user_fname, last_name=user_lname, email=user_email, password=hash)
        user.save()
        return Response(status=201)


@api_view(['POST'])
@authentication_classes([])
def loginUser(request):
    user_email = request.data.get('email')
    user_password = request.data.get('password')

    try:
        checkUser = Users.objects.get(email=user_email)
        verify = ph.verify(checkUser.password, user_password)
        if not verify:
           return Response(status=401)
        else:
            refresh = RefreshToken.for_user(checkUser)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
    except:
        return Response(status=401)
    

@api_view(['POST'])
def createSession(request):
    session_Name = request.data.get('session_Name')
    user = request.user.id
    session = Sessions(user_id_id=user, session_name=session_Name)
    try:
        checkSessionExist = Sessions.objects.get(user_id_id=user, session_name=session_Name) 
        return Response({'Error': 'Session name is not unique'}, status=403)
    except:
        session.save()
        session_id = Sessions.objects.get(user_id_id=user, session_name=session_Name)
        client_fname = request.data.get('fname')
        client_lname = request.data.get('lname')
        print('here2')
        client = Interviewees(first_name=client_fname, last_name=client_lname, session_id_id=session_id.id)
        client.save()
        return Response(status=200)


@api_view(['POST'])
def deleteSession(request):
    user = request.user.id
    session_id = request.data.get('session_id')
   
    try:
        session = Sessions.objects.get(user_id_id=user, id=session_id)
        session.delete()
    except:
        return Response(status=401)
    
    return Response(status=200)


@api_view(['GET'])
def getSessionList(request):
    user = request.user.id
    sessionList = Sessions.objects.filter(user_id_id=user).values('id','session_name', 'transcription', 'summarisation')
    print(sessionList)
    return Response({'data': sessionList}, status=200)


@api_view(['POST'])
def getSummary(request):
    user = request.user.id
    session_id = request.data.get('session_id')

    try:
        session = Sessions.objects.get(id=session_id, user_id_id=user)
        text = summaryFunction(session.transcription)
        session.summarisation = text
        session.save()
        return Response({'Summary': text}, status=200)
    except:
        return Response(status=401)
    


@api_view(['POST'])
def transcribe(request):
    user = request.user.id
    session_id = request.data.get('session_id')
    blob = request.FILES['audio'] 
    tempAudioFile = 'chunk_audio.wav'

    # write audio blob into a audio file
    with open(tempAudioFile, 'wb+') as destination:
        for chunk in blob.chunks():
            destination.write(chunk)
    
    # whisper transcription process
    result = model.transcribe(tempAudioFile, condition_on_previous_text=False, word_timestamps=True, hallucination_silence_threshold=4, fp16=False, language="en")

    print("Whisper:",result["text"])

    try:
        session = Sessions.objects.get(id=session_id, user_id_id=user)
        if session.transcription is None:
            session.transcription = result["text"]
        else:
            session.transcription += result["text"]
        
        session.save()
    except:
        return Response(status=401)

    text = result["text"]
    return Response({'transcription':text}, status=200)
        
