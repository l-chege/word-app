from flask import Flask, request, render_template
import openai
import os
from twilio.rest import Client

import random
from dotenv import load_dotenv

app = Flask(__name__)

openai.api.key = os.getenv("OPENAI_API_KEY")
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
