import urllib3
import json


http = urllib3.PoolManager()

TOKEN = open('token.txt', 'r').read()
url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN

# send the text message to the user, and return the whole response from urllib3
def send_text_message(id, text):
    
    body_dict = {
        "recipient":{"id":id},
        "message":{"text":text}
    }
    "Content-Type: application/json"
    res = http.request( 'POST', url, fields=body_dict, headers={"Content-Type": "application/json"})
    return res

def send_button_message(id, text, typ):
def send_button_message(id, text, title1, title2):
    
    body_dict = {
        "recipient":{"id":id},
        "message":{"attachment":{"type":"template",
            "payload":{"template_type":"button","text":text,
            "buttons":[
                {
                "type":"postback",
                "title":title1,
                "payload":"USER_DEFINED_PAYLOAD"
                },
                {
                "type":"postback",
                "title":title2,
                "payload":"USER_DEFINED_PAYLOAD"
                }
            ]
        }}}
    }
    res = http.request( 'POST', url, fields=body_dict, headers={"Content-Type": "application/json"})
    return res