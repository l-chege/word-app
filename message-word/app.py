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

# static list of affirmations
affirmations = [
    "You are capable of amazing things!",
    "You are enough!",
    "You are loved!",
    "You are doing great!",
    "You are strong!",
    "You are worthy of happiness!",
    "You are a unique and special individual!"
]

# function to generate random affirmation
def generate_affirmation():
    return random.choice(affirmations)

# renders index.html template
@app.route('/')
def home():
    return render_template('index.html')

# triggered when user submits a form with their phone number
@app.route('/send_affirmation', methods=['POST'])
def send_affirmation():
    recipient_number = request.form['phone_number']
    affirmation = generate_affirmation()

    try:
        message = twilio_client.messages.create(
            body=affirmation,
            from_=twilio_phone_number,
            to=recipient_number
        )
        return "Affirmation sent successfully!"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)