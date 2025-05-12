import sparknlp
from sparknlp.pretrained import PretrainedPipeline
from pyspark.sql import SparkSession

# Start Spark NLP Session
spark = sparknlp.start()

# Create a DataFrame with text to summarize
data = [
    (1, "Google has announced the release of a beta version of the popular TensorFlow machine learning library"),
    (2, "Donald John Trump (born June 14, 1946) is the 45th and current president of the United States"),
    (3, "so just need to confirm the spelling of your name. I've got S-K-Y-E as the first name. And then I've got the surname W-H-I-T-E-L-E-Y. Okay, do you have any middle names? Marie."),
    (4, "Number 4 Fleet Street, sorry, number 5 Fleet Street, North Parramatta. I think it's 2152")
]
columns = ["id", "text"]
testData = spark.createDataFrame(data, columns)

# Load pretrained pipeline
pipeline = PretrainedPipeline("explain_document_dl", lang="en")

# Apply pipeline to dataframe
annotation = pipeline.transform(testData)

# Show results
annotation.select("text", "entities.result").show(truncate=False)
