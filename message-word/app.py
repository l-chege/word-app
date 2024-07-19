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

# renders index.html template
@app.route('/')
def home():
    return render_template('index.html')

"""
Updated the route '/send_affirmation' - implemented OpenAI API to dynamically generate affirmations and include error handling. 
The previous implementation had a predefined list of affirmations.
Removed the list of affirmations and function to generate random affirmation as well (no longer needed).

"""
# triggered when user submits a form with their phone number
@app.route('/send_affirmation', methods=['POST'])
def send_affirmation():
    recipient_number = request.form['phone_number']

    try:
        # generate affirmation using OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Give me a positive affirmation.",
            max_tokens=50
        )
        affirmation = response.choices[0].text.strip()

        # Send affirmation via Twilio
        twilio_client.messages.create(
            body=affirmation,
            from_=twilio_phone_number,
            to=recipient_number
        )

        return "Affirmation sent successfully!"
    
    except openai.error.OpenAIError as e:
        # handle OpenAI API errors
        return f"Error generating affirmation: {e}"
    
    except Exception as e:
        # handle general errors
        return f"An error occurred: {e}"
        
if __name__ == '__main__':
    app.run(debug=True)