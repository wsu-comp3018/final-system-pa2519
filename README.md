# Statement Creation Tool

# Project Description
A tool to write statements in real time as an interview with a witness is taking place either face to face, or remotely. This tool would have utility for any type of investigative field that involves the collection of statements, affidavits or Stat Decs including insurance, policing, legal.

This is more sophisticated transcription tool. It would not simply transcribe the entire exchange between the witness and interviewer. It would only write words that would be attributable to the witness in their statement, taken directly from their answers to the questions. This might be done by the interviewer listening to the answer and then dictating a statement paragraph on behalf of the witness. Or, if it were quite sophisticated, the tool could convert the witness’s answer into a statement sentence that matches the style of the statement, having learned it from past experience, without the interviewer having to directly dictate.

# Requirements

Your system should have the following installed:

- **Python 3.13**
- **Node.js (v18 or later)**
- **pipenv**
- **FFmpeg** (required for Whisper transcription)
- **Git**

Several install need to occur for the front-end and back-end. These are split into the following sections:

# Front-End Setup

Built with **Nuxt.js** (Vue 3)

- cd into the front-end folder
- npm install
- npm run dev

# Back-End
Install pipenv
- pip install pipenv (if not installed)

Install dependencies 
- cd into the back-end folder
- pip install

This installs Django, Django REST Framework, CORS Headers, JWT Auth, Whisper, Spark NLP + Pyspark, Transformers (with Torch), Argon2, Jinja2, Numpy and hf-xet

Activate Virtual Environment
for Windows:
- pipenv shell

for Mac:
python3.11 -m venv venv
source venv/bin/activate

Run Migrations and Server
- python manage.py migrate
- python manage.py runserver

# Back-End (Individual Installs)
If required, install each dependency individually with the following:
**Django**

pip install django

**Django REST Framework**

pip install djangorestframework

**Django CORS Headers**

pip install django-cors-headers

**Simple JWT Authentication for DRF**

pip install djangorestframework-simplejwt

**Whisper**

pip install -U openai-whisper

**Spark NLP**

pip install spark-nlp==5.5.3

**PySpark**

pip install pyspark

**HuggingFace Transformers with Torch support**

pip install "transformers[torch]"

**Argon2 Password Hasher**

pip install argon2-cffi

**Jinja2 Template Engine**

pip install jinja2

**NumPy**

pip install numpy

**HuggingFace Xet (hf-xet)**

pip install hf-xet



