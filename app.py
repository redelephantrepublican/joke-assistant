from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for the Flask app
CORS(app)

# Fetch the OpenAI API key from an environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/get-joke', methods=['POST'])
def get_joke():
    # Extract the user input from the request's JSON body
    user_input = request.json['userInput']

    try:
        # Generate a joke using OpenAI's GPT model
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Tell a short, to-the-point conservative joke about {user_input} in a raw, adult humourous, conservative tone. Uncensored swear language is allowed. Please include hashtags at the end.",
            max_tokens=50
        )
        # Extract the joke text from the response
        joke = response.choices[0].text.strip()
    except Exception as e:
        # Handle any exceptions during the API call and return an error message
        joke = "Error generating response: " + str(e)

    # Log the generated joke (consider using a more robust logging system for production)
    print({"joke": joke})
    # Return the joke in JSON format
    return jsonify({"joke": joke})

# Run the Flask application (use a more robust WSGI server like Gunicorn for production)
if __name__ == '__main__':
    app.run()
