from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken
import whisper
from summariser.views import summaryFunction
import zipfile
import os
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
# from .serializers import StatementTemplateSerializer
from rest_framework import viewsets
from .forms import uploadTemplates
from django.shortcuts import render
from django.http import JsonResponse

ph = argon2.PasswordHasher()
model = whisper.load_model("base")

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
def createAccount(request):
    user_fname = request.data.get('fname').strip()
    user_lname = request.data.get('lname').strip()
    user_email = request.data.get('email').strip()
    user_password = request.data.get('password').strip()
    
    hash = ph.hash(user_password)

    try:
        userExist = Users.objects.get(email=user_email)
        return Response(status=409)
    except:
        userObj = Users(first_name=user_fname, last_name=user_lname, email=user_email, password=hash)
        userObj.save()
        return Response(status=201)

  

@api_view(['POST'])
@authentication_classes([])
def loginUser(request):
    user_email = request.data.get('email').strip()
    user_password = request.data.get('password').strip()

    try:
        userObj = Users.objects.get(email=user_email)
        verify = ph.verify(userObj.password, user_password)
        if not verify:
           return Response(status=401)
        else:
            refresh = RefreshToken.for_user(userObj)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
    except:
        return Response(status=401)
    

@api_view(['POST'])
def createSession(request):
    session_Name = request.data.get('session_name').strip()
    user = request.user.id
    sessionObj = Sessions(user_id_id=user, session_name=session_Name)
    try:
        checkSessionExist = Sessions.objects.get(user_id_id=user, session_name=session_Name) 
        return Response({'Error': 'Session name is not unique'}, status=403)
    except:
        sessionObj.save()
        session_id = sessionObj.id
        client_fname = request.data.get('fname').strip()
        client_lname = request.data.get('lname').strip()
        clientObj = Interviewees(first_name=client_fname, last_name=client_lname, session_id_id=session_id)
        clientObj.save()
        return Response(status=200)


@api_view(['POST'])
def deleteSession(request):
    user = request.user.id
    session_id = request.data.get('session_id')
   
    try:
        sessionObj = Sessions.objects.get(user_id_id=user, id=session_id)
        sessionObj.delete()
    except:
        return Response(status=401)
    
    return Response(status=200)


@api_view(['GET'])
def getSessionList(request):
    user = request.user.id
    sessionList = Sessions.objects.filter(user_id_id=user).values('id','session_name', 'transcription', 'summary')
    #print(sessionList)
    return Response({'data': sessionList}, status=200)


@api_view(['POST'])
def getSummary(request):
    user = request.user.id
    session_id = request.data.get('session_id')

    try:
        sessionObj = Sessions.objects.get(id=session_id, user_id_id=user)
        text = summaryFunction(sessionObj.transcription)
        if text is None: # if no transcription, it will stop execution
            return Response(status=500)
        sessionObj.summary = text
        sessionObj.save()
        return Response({'summary': text}, status=200)
    except:
        return Response(status=401)
    

@api_view(['POST'])
def test(request):
    user = request.user.id
    statement_id = 7

    try:
        x = Statements.objects.get(user_id_id = user, id= statement_id)
        x.delete()
        return Response(status=200)
    except:
        return Response(status=401)

@api_view(['POST'])
def generateStatement(request):
    user = request.user.id
    sessionID = request.data.get('session_id')
    try:
        clientObj = Interviewees.objects.get(session_id=sessionID)
        sessionObj = Sessions.objects.get(id=sessionID, user_id_id=user)

        text = summaryFunction(sessionObj.transcription)
        if text is None:
            return Response(status=401)

        statement = Statements(user_id_id=user, interviewee_id_id=clientObj.id, statement_content=text)
        statement.save()
        return Response({'statement_id': statement.id}, status=200)
        
    except:
        return Response(status=500)
    

@api_view(['POST'])
def getStatement(request):
    user = request.user.id
    statement_id = request.data.get('statement_id')
    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        content = statementObj.statement_content
        return Response({'statement': content}, status=200)
    except:
        return Response(status=401)
    
@api_view(['GET'])
def getStatementList(request):
    user = request.user.id

    try:
        statementObj = Statements.objects.filter(user_id_id = user)
        clientList = []
        for obj in statementObj:
            client = Interviewees.objects.get(id = obj.interviewee_id_id)
            dict = {
                'statement_id': obj.id,
                'client_first_name': client.first_name,
                'client_last_name': client.last_name,
            }
            clientList.append(dict)
        return Response({'list': clientList},status=200)
    except:
        return Response(status=401)


@api_view(['POST'])
def updateStatement(request):
    user = request.user.id
    statement_id = request.data.get('statement_id')
    updated_statement = request.data.get('updated_statement')

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.statement_content = updated_statement
        statementObj.save()
        return Response(status=200)
    except:
        return Response(status=401)
    

@api_view(['POST'])
def deleteStatement(request):
    user = request.user.id
    statement_id = request.data.get('statement_id')

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.delete()
        return Response(status=200)
    except:
        return Response(status=401)
    
    
@api_view(['POST'])
def uploadRecordings(request):
    sessionID = request.data.get('session_id')
    name = request.data.get('audio_name')
    fullRecording = request.FILES['fullRecording']

    audioObj = AudioRecordings(session_id_id = sessionID, audio_name = name, audio_path = fullRecording)
    audioObj.save()
    
    return Response(status=200)

# WORKING BUT DISABLED FOR NOW
# @api_view(['POST'])
# def downloadRecording(request):
#     sessionID = request.data.get('session_id')

#     try:
#         audioObjs = AudioRecordings.objects.filter(session_id_id = sessionID)
#         with zipfile.ZipFile('audioRecordings.zip', 'w') as myZipFile:
#             for audio in audioObjs:
#                 myZipFile.write(audio.audio_path.path, os.path.basename(audio.audio_path.path))
        
#         print('here')
#         return FileResponse(open('audioRecordings.zip', 'rb'), as_attachment=True, status=200)
#         #return Response(status=200)
#     except:
#         print("error")
#         return Response(status=500)

@api_view(['POST'])
def templateUpload(request):


    if request.method=="POST":
        template=uploadTemplates(request.POST,request.FILES)
        if template.is_valid():
            template.save()

            return Response({"message": "File Upload Successful!"},status=201)
        return Response({"error": "Error! Problem in uploading!"}, status=400)
    

        

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
    print("transcribing")
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
        
