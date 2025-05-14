import os
from transformers import pipeline
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("Open-Source Summarization") \
    .config("spark.driver.memory", "4G") \
    .getOrCreate()

# Read input file
with open("document.txt", "r") as f:
    text = f.read()

# Split text into chunks of ~500 words (optional for large texts)
def split_into_chunks(text, max_words=500):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

chunks = split_into_chunks(text)

# Load HuggingFace summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Summarize each chunk and join results
summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
             for chunk in chunks]

final_summary = "\n".join(summaries)

print("\n📄 Summary:\n")
print(final_summary)
