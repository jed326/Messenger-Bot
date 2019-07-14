#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os
import pickle
import ngram

with open('Model/JayDeng.pkl') as file:
    model = pickle.load(file)
app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


# The base route for Facebook webhook
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        '''
        Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.
        '''
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Store Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        text = message['message'].get('text')
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)

                    # If user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    '''
    Compare the VERIFY_TOKEN sent from Facebook to our local one.
    '''
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    # sample_responses = [
    #     "I have the power of god and anime on my side!", "I love salmon.",
    #     "Area 51", "YEEEEEET"
    # ]
    # # return selected item to the user
    # return random.choice(sample_responses)
    return model.random_text(15)


# pymessenger send function
def send_message(recipient_id, response):
    '''
    sends user the text message provided via input response parameter
    '''
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()