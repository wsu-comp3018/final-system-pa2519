from rest_framework.response import Response
from rest_framework import status
from .models import *

from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken
import whisper
from summariser.views import summaryFunction
from statement.views import generate_statement
from rest_framework.permissions import IsAuthenticated
# from .serializers import StatementTemplateSerializer
from .forms import uploadTemplates



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
    

    try:
        userObj = Users.objects.get(id = user)
        if email != '':
            userObj.email = email
        
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
def generateStatement(request):
    user = request.user.id
    sessionID = request.data['session_id']
    try:
        clientObj = Interviewees.objects.get(session_id=sessionID)
        sessionObj = Sessions.objects.get(id=sessionID, user_id_id=user)
        templateObj = StatementTemplates.objects.get(id = 1)

        transcription = sessionObj.transcription.strip()
        text = generate_statement(transcription, templateObj.template_path.path)

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
def uploadRecording(request):
    sessionID = request.data['session_id']
    name = request.data['audio_name']
    fullRecording = request.FILES['fullRecording']

    audioObj = AudioRecordings(session_id_id = sessionID, audio_name = name, audio_path = fullRecording)
    audioObj.save()
    
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
    result = model.transcribe(tempAudioFile, condition_on_previous_text=False, word_timestamps=True, hallucination_silence_threshold=4, fp16=False, language="en")

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
        
