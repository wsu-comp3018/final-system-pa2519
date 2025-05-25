import os
from transformers import pipeline

# Create your views here.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def summaryFunction(transcription):

    # Get transcription
    text = transcription

    # Split text into chunks of ~500 words (optional for large texts)
    def split_into_chunks(text, max_words=100):
        words = text.split()
        return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

    chunks = split_into_chunks(text)

    # Load HuggingFace summarizer
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Summarize each chunk and join results
    summaries = [summarizer(chunk, max_length=65, min_length=30, do_sample=False)[0]['summary_text']
                for chunk in chunks]

    final_summary = "\n".join(summaries)

    print(final_summary)

    return final_summary