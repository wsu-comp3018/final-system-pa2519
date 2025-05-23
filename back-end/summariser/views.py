import os
from transformers import pipeline
from pyspark.sql import SparkSession

# Create your views here.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def summaryFunction(transcription):
    print('transcription', transcription)

    print('got text')
    # Get transcription
    text = transcription

    print('here')
    # Split text into chunks of ~500 words (optional for large texts)
    def split_into_chunks(text, max_words=100):
        words = text.split()
        return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

    print('here2')
    chunks = split_into_chunks(text)

    print('here')
    # Load HuggingFace summarizer
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Summarize each chunk and join results
    summaries = [summarizer(chunk, max_length=30, min_length=30, do_sample=False)[0]['summary_text']
                for chunk in chunks]

    final_summary = "\n".join(summaries)

    print(final_summary)

    return final_summary