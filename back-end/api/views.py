from rest_framework.response import Response
from rest_framework import status
from .models import *

from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken
import whisper
from summariser.views import summaryFunction
from statement.views import generate_statement
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
    user_fname = request.data['fname'].strip()
    user_lname = request.data['lname'].strip()
    user_email = request.data['email'].strip()
    user_password = request.data['password'].strip()
    
    hash = ph.hash(user_password)

    try:
        userExist = Users.objects.get(email=user_email)
        return Response(status=409)
    except:
        userObj = Users(first_name=user_fname, last_name=user_lname, email=user_email, password=hash)
        userObj.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def deleteAccount(request):
    user = request.user.id
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception as e:
            return Response({"error": "problem invalidating token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


    try:
        userObj = Users.objects.get(id = user)
        userObj.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['POST'])
def updateAccountDetails(request):
    user = request.user.id
    email = request.data['email']
    current_password = request.data['current_password']
    new_password = request.data['new_password']
    
    print('password',current_password)

    try:
        userObj = Users.objects.get(id = user)
        print('here')
        if email != '':
            userObj.email = email
            print('email')
        
        if current_password != '':
            try:
                ph.verify(userObj.password, current_password)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            hash = ph.hash(new_password)
            userObj.password = hash
        
        userObj.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

@api_view(['POST'])
@authentication_classes([])
def loginUser(request):
    user_email = request.data['email'].strip()
    user_password = request.data['password'].strip()

    try:
        userObj = Users.objects.get(email=user_email)
        ph.verify(userObj.password, user_password)
        refresh = RefreshToken.for_user(userObj)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="api_token", value = str(refresh.access_token), samesite=None, secure=True)
        response.set_cookie(key="refresh_token", value = str(refresh), httponly=True, samesite=None, secure=True)

        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logoutUser(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception as e:
            return Response({"error": "problem invalidating token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def getAccountSettings(request):
    user = request.user.id

    try:
        userObj = Users.objects.get(id = user)
        userData = {
            'first_name': userObj.first_name,
            'last_name': userObj.last_name,
            'email': userObj.email,
        }

        return Response({'user': userData}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def createSession(request):
    session_Name = request.data['session_name'].strip()
    user = request.user.id
    sessionObj = Sessions(user_id_id=user, session_name=session_Name)
    try:
        checkSessionExist = Sessions.objects.get(user_id_id=user, session_name=session_Name) 
        return Response({'Error': 'Session name is not unique'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        sessionObj.save()
        session_id = sessionObj.id
        client_fname = request.data['fname'].strip()
        client_lname = request.data['lname'].strip()
        client_email = request.data['email'].strip
        clientObj = Interviewees(first_name=client_fname, last_name=client_lname, session_id_id=session_id, email=client_email)
        clientObj.save()
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def deleteSession(request):
    user = request.user.id
    session_id = request.data['session_id']
   
    try:
        sessionObj = Sessions.objects.get(user_id_id=user, id=session_id)
        sessionObj.delete()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def getSessionList(request):
    user = request.user.id
    sessionList = Sessions.objects.filter(user_id_id=user).values('id','session_name', 'transcription', 'summary')
    return Response({'data': sessionList}, status=status.HTTP_200_OK)



@api_view(['POST'])
def getSummary(request):
    user = request.user.id
    session_id = request.data['session_id']

    try:
        sessionObj = Sessions.objects.get(id=session_id, user_id_id=user)
        print('here')
        transcription = sessionObj.transcription.strip()
        text = summaryFunction(transcription)
        if text is None: # if no transcription, it will stop execution
            return Response(status=500)
        sessionObj.summary = text
        sessionObj.save()
        return Response({'summary': text}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def test(request):
    user = request.user.id
    sessionID = 1

    try:
        x = Sessions.objects.get(id = sessionID, user_id_id = user)
        x.transcription = '''Claimant's name is J-O-E-L and he has a surname W-H-I-T-E-L-E-Y. He is single and has no dependent children. He was injured in a non-work accident, such as at home.\
He is 22 years old and was born on the 20-09-2002
My phone number is 0491130126 and my email is abc@gmail.com
I work as a sales assistant
I currently work at EML Insurance
I had a hematoma and a hairline fracture in my femur. I've never actually had it x-rayed or looked at. It's just sort of swells up every now and then.  for 10 years, but it was cosmetic nursing in a private clinic.\
"I did the business I work for now, I've moved into like I've worked for different RTOs before this one. I don't know if that is relevant. Oh, so that was a different employer? Yes. And did that job involve much manual handling or heavy lifting? No" "My break is half an hour of unpaid lunch break"\
Worked with her at the previous employment and national training organization. Has received any further training or refresher training that's addressed manual handling or safe lifting technique.\
I liaise with clients, either via phone or email. I speak to our trainers via phone and email, doing a lot of paperwork. It's mostly admin-based sitting in front of my computer. Have you ever made any complaints or raised any concern about any of your duties?\
I was attempting to pick up a box of paperwork from the floor. I felt twinge in my lower back very sudden and kind of felt like nerve pain when shooting down my leg. And it affected my movement.\
I was concerned that someone would injure themselves picking it up and putting it up on the desk. I always bend with my knees and try not to use my back to lift. I know I have to really brace myself to do it.\
I was under a lot of pressure with some work tasks that I needed to get done. I also am hesitant to contact her while she's on maternity leave because I know she's busy with her baby. She told me to rest up and to give her an update tomorrow morning on how I was feeling.\
I had the ultrasound on the same day as you saw the doctor, as you spoke to the doctor on the phone? Yes, I did. And when did you become aware of the results of the ultrasound? I think it was like three or four days later when I had a follow-up call with the GT. And you were referred for anything else, any physio or anything else? Yeah. I did get a referral for a physio as well. Do you know the name of the actual practitioner? His name is Joe.\
I picked up a box. I didn't realise I had to tell him that happened at work for it to be. a workers' compensation thing. I waited around two weeks to make the claim as I wasn't 100% sure of the whole process and I couldn't get in touch with my manager. She was fine with it. I think she was a little bit surprised that I was still in pain.\
I hope maybe you might get that paid back. I still have the pain every day. It's not as bad, but it does restrict things that I do as just everyday tasks in my life, like put my shoes on and bending over in the shower and things like that. I've been catching the tram because I can't walk as far anymore.\
Do you have any text messages or anything in writing in which you refer to the incident, preferably closer to the day of the incident? And this can be text to anyone, your partner, friends, family. Do you know if you did mislead, make an incident report of this, or did she have you make a report?
I was a Systems Administrator
'''
        x.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     x = AudioRecordings.objects.all()
    #     for y in x:
    #         print(y.audio_path)
    #     return Response(status=status.HTTP_200_OK)
    # except:
    #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generateStatement(request):
    user = request.user.id
    sessionID = request.data['session_id']
    try:
        clientObj = Interviewees.objects.get(session_id=sessionID)
        sessionObj = Sessions.objects.get(id=sessionID, user_id_id=user)
        templateObj = StatementTemplates.objects.get(id = 1)

        transcription = sessionObj.transcription.strip()
        text = generate_statement(transcription, templateObj.template_path.path)

        textfile = 'test_text.txt'

        with open(textfile, 'w') as file:
            file.write(text)

        if text is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        statement = Statements(user_id_id=user, interviewee_id_id=clientObj.id, statement_content=text)
        statement.save()
        return Response({'statement_id': statement.id}, status=status.HTTP_200_OK)
        
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
def getStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']
    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        content = statementObj.statement_content
        return Response({'statement': content}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


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
                'statement_content': obj.statement_content,
            }
            clientList.append(dict)
        return Response({'list': clientList},status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def updateStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']
    updated_statement = request.data['updated_statement']

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.statement_content = updated_statement
        statementObj.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def deleteStatement(request):
    user = request.user.id
    statement_id = request.data['statement_id']

    try:
        statementObj = Statements.objects.get(id = statement_id, user_id_id = user)
        statementObj.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def uploadRecordings(request):
    sessionID = request.data['session_id']
    name = request.data['audio_name']
    fullRecording = request.FILES['fullRecording']

    audioObj = AudioRecordings(session_id_id = sessionID, audio_name = name, audio_path = fullRecording)
    audioObj.save()

    print(audioObj.audio_path)
    
    return Response(status=status.HTTP_200_OK)

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
    session_id = request.data['session_id']
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
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    text = result["text"]
    return Response({'transcription':text}, status=status.HTTP_200_OK)
        
