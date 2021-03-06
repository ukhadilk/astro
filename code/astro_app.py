from flask import Flask, request
from flask import send_from_directory
import os
import json
import requests
import util
import logging as log

app = Flask(__name__)
config_dict = util.get_configs()


@app.route('/privacy/', methods=['GET'])
def return_privacy_page():
    pass


@app.route('/', methods=['GET'])
def verification_get_method():
    if request.args.get('hub.verify_token', '') == \
            config_dict['VERIFICATION_TOKEN']:
        print "Verification successful!"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed!"
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def read_respond_messages():
    print "Handling Messages"
    payload = request.get_data()
    print payload
    for usr_id, message_text in messaging_events(payload):
        print "Incoming from %s: %s" % (usr_id, message_text)


    return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  message_cluster = data["entry"][0]["messaging"]
  for message_data in message_cluster:
    if "message" in message_data and "text" in message_data["message"]:
      yield message_data["sender"]["id"], \
            message_data["message"]["text"].encode('unicode_escape')
    else:
      yield message_data["sender"]["id"], ""


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """
  print "Sending Message: ", text, "recipient: " + recipient
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
