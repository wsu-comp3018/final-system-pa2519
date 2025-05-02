from django.shortcuts import render
from django.http import HttpResponse
import whisper
from django.views.decorators.csrf import csrf_exempt 


# Create your views here.
@csrf_exempt 
def transcribe(request):
    if (request.method == 'POST'): # Check request method is POST
        blob = request.FILES['audio'] # Get audio blob object from request
        tempAudioFile = 'chunk_audio.wav'

        # write audio blob into a audio file
        with open(tempAudioFile, 'wb+') as destination:
            for chunk in blob.chunks():
                destination.write(chunk)
        
        # whisper transcription process
        print("Transcribing")
        model = whisper.load_model("base")
        result = model.transcribe(tempAudioFile, condition_on_previous_text=False, word_timestamps=True, hallucination_silence_threshold=4, fp16=False, language="en")

        print("Whisper:", result["text"])

        return HttpResponse(result["text"], content_type="text/plain")
