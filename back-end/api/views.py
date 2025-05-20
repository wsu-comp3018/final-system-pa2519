from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view, authentication_classes
import argon2
from rest_framework_simplejwt.tokens import RefreshToken

ph = argon2.PasswordHasher()
# Create your views here.
@api_view(['POST'])
@authentication_classes([])
def createAccount(request):
    user_fname = request.data.get('fname')
    user_lname = request.data.get('lname')
    user_email = request.data.get('email')
    user_password = request.data.get('password')
    print(user_fname, user_lname, user_email, user_password)
    
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

# PLEASE IGNORE FOR NOW, WILL IMPLEMENT AT A LATER DATE
# def transcribe(request):
#     if (request.method == 'POST'): # Check request method is POST
#         blob = request.FILES['audio'] # Get audio blob object from request
#         tempAudioFile = 'chunk_audio.wav'

#         # write audio blob into a audio file
#         with open(tempAudioFile, 'wb+') as destination:
#             for chunk in blob.chunks():
#                 destination.write(chunk)
        
#         # whisper transcription process
#         print("Transcribing")
#         model = whisper.load_model("base")
#         result = model.transcribe(tempAudioFile, condition_on_previous_text=False, word_timestamps=True, hallucination_silence_threshold=4, fp16=False, language="en")

#         print("Whisper:", result["text"])

#         return Response({transcription: result["text"]})
        
