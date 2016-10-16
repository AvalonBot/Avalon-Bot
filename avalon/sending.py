import urllib3
import json
import threading
import os.path
from .playerio import *

urllib3.disable_warnings()
http = urllib3.PoolManager()

TOKEN = open( os.path.dirname(os.path.realpath(__file__)) + '/token.txt', 'r' ).read()
welcome = 'retard as shit' # Nice one

thread_pool = []
thread_option = False


def send_req(method, url, body, headers):
    res = http.request( method, url, body=body, headers=headers )
    check(res)
   
# deprecated 
def start_sending(method, url, body, headers):
    if thread_option:
        t = threading.Thread( target = send_req, args = (method, url, body, headers) )
        thread_pool.append( t )
        t.start()
    else:
        send_req(method, url, body, headers)
        
def send_text_message_id(the_id, text):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    body_dict = {
        "recipient":{"id":the_id},
        "message":{"text":text}
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    res = http.request( 'POST', url, body=encoded_data, headers={'Content-Type': 'application/json'} )
    check(res)

# send the text message to the user, and return the whole response from urllib3
def send_text_message( player, text):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    
    body_dict = {
        "recipient":{"id":player.id},
        "message":{"text":text}
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    '''
    res = http.request( 'POST', url, body=encoded_data, headers={'Content-Type': 'application/json'} )
    check(res)
    '''
    send_to_queue( player, ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )

# send message with buttons to the user, and return the whole response from urllib3    
def send_button_message(user_id, text, title1=None, title2=None, title3=None):
    
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    
    the_btns = []
    # payload should be carefully defined to maximumize the efficiency
    '''
    {
        "type":"postback",
        "title":title1,
        "payload":"USER_DEFINED_PAYLOAD"
    }
    '''
    
    body_dict = {
        "recipient":{"id":user_id},
        "message":{"attachment":{"type":"template",
            "payload":{"template_type":"button","text":text,
            "buttons":the_btns
        }}}
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    
    #start_sending( 'POST', url, encoded_data, {'Content-Type': 'application/json'})
    send_to_queue( player, ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )

# ask all people if they agree with the chosen team to go on a mission
def send_vote_choice_all( game ):
    for player_id in game.players.keys():
        send_vote_choice( player_id, game )

# ask a person if he/she agrees with the chosen team to go on a mission
def send_vote_choice( voter_id, game ):
    '''
    Payload format : voting-<game_number>-<yes or no>
    '''
    
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN

    body_dict = {
        "recipient":{"id":voter_id},
        "message":{"text":'Do you agree to let these people go on a mission?',
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Fuck yeah",
                    "payload":"voting-"+str(game.Game_num)+"-yes"
                },
                {
                    "content_type":"text",
                    "title":"Hell no",
                    "payload":"voting-"+str(game.Game_num)+"-no"
                }
            ]
        }
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    #start_sending( 'POST', url, encoded_data, {'Content-Type': 'application/json'})
    send_to_queue( game.players[voter_id], ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )

# ask the current commander to choose his/her team for next mission
def send_people_choice( game, player_list ):
    '''
    For commander to choose who to carry out the mission
    player_list includes the user id
    Payload format : sendppl-<game_number>-<player_id>
    '''
    #game.players[ <play_id> ].name can get the name of users
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    the_btns = []
    for the_person in player_list:
        the_btns.append({
        "content_type":"text",
        "title":game.players[the_person].name,
        "payload":"sendppl-"+game.Game_num+"-"+the_person
    })
    body_dict = {
        "recipient":{"id":game.commander},
        "message":{"text":'Choose a person for the mission',
            "quick_replies":the_btns
        }
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    
    send_to_queue( game.players[game.commander], ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )
    
    # start_sending( 'POST', url, encoded_data, {'Content-Type': 'application/json'})

def ass_kill_choice( game,the_id, player_list ):
    '''
    For Assassin to guess who is Melin
    player_list includes the user id
    Payload format : asskill-<game_number>-<player_id>
    '''
    #game.players[ <play_id> ].name can get the name of users
    
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    the_btns = []
    for the_person in player_list:
        the_btns.append({
            "content_type":"text",
            "title":game.players[the_person].name,
            "payload":"asskill-"+str(game.Game_num)+"-"+the_person
        })
    print('creating dict')
    body_dict = {
        "recipient":{"id":the_id},
        "message":{"text":'Guess which one is Merlin.',
            "quick_replies":the_btns
        }
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    print('sending the buttons')
    res = http.request( 'POST', url, headers={'Content-Type': 'application/json'}, body=encoded_data )
    check( res )
    
def godness_choice( game,the_id, player_list ):
    '''
    For Commander to ask Godness people's side
    player_list includes the user id
    Payload format : godness-<game_number>-<player_id>
    '''
    #game.players[ <play_id> ].name can get the name of users
    
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    the_btns = []
    for the_person in player_list:
        the_btns.append({
            "content_type":"text",
            "title":game.players[the_person].name,
            "payload":"godness-"+str(game.Game_num)+"-"+the_person
        })
    print('creating dict')
    body_dict = {
        "recipient":{"id":the_id},
        "message":{"text":'Choose one to check out which side does he belongs.',
            "quick_replies":the_btns
        }
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    print('sending the buttons')
    '''
    res = http.request( 'POST', url, headers={'Content-Type': 'application/json'}, body=encoded_data )
    check( res )
    '''
    send_to_queue( game.players[the_id], ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )
    
    
# ask a mission team member to decide success/failure    
def send_mission_choice( voter_id, game ):
    '''
    To let a chosen person decide whether to let the mission success
    Payload format : mission-<game_number>-<success or fail>
    '''
    print("sending mission choice to team")
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + TOKEN
    body_dict = {
        "recipient":{"id":voter_id},
        "message":{"text":'Will you let the mission succeed? (Hint: Only bad guys can choose to fail the mission)',
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Of course!",
                    
                    "payload":"mission-"+str(game.Game_num)+"-success"
                },
                {
                    "content_type":"text",
                    "title":"Fuck it!",
                    "payload":"mission-"+str(game.Game_num)+"-fail"
                }
            ]
        }
    }
    print("button generated to " + voter_id)
    encoded_data = json.dumps(body_dict).encode('utf-8')
    #res = http.request( 'POST', url, headers={'Content-Type': 'application/json'}, body=encoded_data )
    #check(res)
    
    send_to_queue( game.players[voter_id], ( 'POST', url, encoded_data, {'Content-Type': 'application/json'} ) )
    
        
# ask all mission team members to decide success/failure    
def send_mission_choice_all( game ):
    '''
    arrange to ask each missioner about whether or not to let a mission success
    '''
    for missioner_id in game.cur_mission.missioners:
        send_mission_choice( missioner_id, game)
        
# announce the choice of the current commander to everyone
def announce_missioners( game ):
    text = "Below is the chosen players:"
    for chosen_player_id in game.cur_mission.missioners:
        text = text + "\n" + game.players[chosen_player_id].name
    announce_text_message( game, text )

# announce the result of the mission
def announce_mission_result( game, bool_result, success_num, fail_num ):
    text = "The current mission has "
    if bool_result:
        text = text + "succeeded\nAll " + str(success_num) + " members have chosen success!"
    else:
        text = text + "failed\nThere are " + str(fail_num) + " failures in the team of " + str(success_num + fail_num)
    announce_text_message( game, text )

# public broadcasting
def announce_text_message( game, text ):
    for player in game.players.values():
        send_text_message( player, text)
        
# broadcasting the chating message
def announce_chat_message( game, player, text ):
    text = player.name + " : " + text
    for recipient in game.players.values():
        if recipient.id != player.id:
            send_text_message( recipient, text)
            
    
# the persistent menu 
def persist_menu():
    
    url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=" + TOKEN
    body_dict = {
        "setting_type" : "call_to_actions",
        "thread_state" : "existing_thread",
        "call_to_actions":[
            {
                "type":"postback",
                "title":"Explain rule",
                "payload":"@exp"
            },
            {
                "type":"postback",
                "title":"My current status",
                "payload":"@?"
            },
            {
                "type":"postback",
                "title":"Let's vote!",
                "payload":"@hurry"
            },
            {
                "type":"postback",
                "title":"Exit game",
                "payload":"@exit"
            }
        ]
    }
    encoded_data = json.dumps(body_dict).encode('utf-8')
    res = http.request( 'POST', url, headers={'Content-Type': 'application/json'}, body=encoded_data )
    check( res )
    
persist_menu()