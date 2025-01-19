

import os
from twilio.rest import Client
from langchain_community.llms import OpenAI  # Updated import
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain_community.chains import ConversationalChain  # Updated import
from flask import Flask, request, jsonify

# Load PDF and create a knowledge base
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

# Initialize OpenAI and Twilio clients
openai_api_key = os.getenv("OPENAI_API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

openai_client = OpenAI(api_key=openai_api_key)
knowledge_base = load_pdf(r"C:\Users\nivia\Downloads\Osteomyelitis-trial pdf.pdf")  # Update with your PDF path
chatbot = ConversationalChain(openai_client, knowledge_base)

# Function to handle incoming messages
def handle_message(incoming_msg):
    response = chatbot.run(incoming_msg)
    return response

# Twilio webhook endpoint
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body")
    response_msg = handle_message(incoming_msg)

    client = Client(twilio_account_sid, twilio_auth_token)
    client.messages.create(
        body=response_msg,
        from_=twilio_phone_number,
        to=request.form.get("From")
    )
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)