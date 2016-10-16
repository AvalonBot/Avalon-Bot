from pyramid.response import Response
from pyramid.view import view_config
import traceback
import sys
from . import status
from . import sending
from . import moves
from . import dealm

ask_to_join = 'Welcome to the Avalon bot game! Please input a # and 6-digit-number to join or create a room (ex. #123456).'
seperate_symbol = [ ' ', ',', '\n', '\t', '.', '&', '/', '-', '_', '\\', '~', '+' ]
bighead = status.Bighead()

'''
        {'entry': [{'messaging': [{'timestamp': 1476548716734, 'recipient': {'id': '1840924172803382'},
 'postback': {'payload': '@exp'}, 'sender': {'id': '1292848977424410'}}], 'id': '18409241728033
82', 'time': 1476548716734}], 'object': 'page'} 
'''

@view_config(route_name='view_webhook')
def view_webhook(req):
    
    the_id = req.json_body['entry'][0]['messaging'][0]['sender']['id']
    print('id : ' + str(the_id) )
    
    #print(req.json_body)
    #[ sending.send_text_message( the_id, sending.welcome ) for i in range(20) ]
    
    if dealm.is_echo(req):
        return Response('echo')

    try:
        print('checking postback')
        payload = req.json_body['entry'][0]['messaging'][0]['postback']['payload']
        print('into postback payload')
        print(payload)
        dealm.deal_postback(the_id, payload, bighead)
        return Response('done')
    except KeyError:
        pass
    except Exception as err:
        traceback.print_tb( sys.exc_info()[2] )
        print( type(err) )
        print( err )
    
    try:
        print('checking quick_reply')
        # try to see if it is a payload message
        payload = req.json_body['entry'][0] ['messaging'][0]['message']['quick_reply']['payload']
        dealm.deal_playload(the_id, payload, bighead)
        return Response('done')
    except KeyError:
        pass
    except Exception as err:
        traceback.print_tb( sys.exc_info()[2] )
        print( type(err) )
        print( err )
    
    # for the part we are dealing is the text part
    
    try:
        try:
            text = req.json_body['entry'][0]['messaging'][0]['message']['text']
        except:
            return Response('No text')
    
        print(text)
        room_num = moves.check_in_room(the_id, bighead)
        
        # See if the person is in any game, if not ask him or her to join one game
        if not room_num:
            if text[0] != '#':
                sending.send_text_message_id( the_id, ask_to_join )
            else:
                for i in seperate_symbol:
                    if i in text:
                        text = text.split(i)
                        break
                    
                tt = text[0][1:]
                name = text[1]
                if len(name) > 20:
                    sending.send_text_message_id( the_id, 'Too LONG la, Marginal.' )
                    return Response('No')

                if tt.isdigit() and len(tt) == 6:
                    moves.IntoGame( the_id, tt, bighead, name )

        else:
            in_game = bighead.game_table[ bighead.player_table[the_id] ]
            assert isinstance( in_game, status.Game )
        
            if text[0] == '@':
                sending.announce_chat_message( in_game, in_game.players[the_id], text[1:] )
            
            if  in_game.status == 'waiting' and in_game.host == the_id and text == 'start':
                # check if the players are enough to launch the game, 
                if in_game.check_enough():
                    in_game.status == 'dark'
                    # assign_Character, let some players know each other
                    moves.day_dark( in_game )
                else:
                    sending.send_text_message( in_game.players[the_id], 'Still not enough people! Minimum number is 5' )
                
            elif in_game.status == 'dark':
                pass
                # no matter what they talk is shit, players should shut the fk up
            elif in_game.status == 'morning' and in_game.commander == the_id:
                # should be implement
            #    choose_missioner()
                pass
            elif in_game.status == 'voting':
                if in_game.host == the_id and text == 'hurry':
                    [sending.send_vote_choice(i, in_game) for i in in_game.players.keys() \
                    if i not in in_game.cur_mission.vote_rec.keys()]
                        
            elif in_game.status == 'conduct' and the_id in in_game.cur_mission.missioners :
                if in_game.host == the_id and text == 'hurry':
                    [sending.send_mission_choice(i, in_game.Game_num) for i in in_game.cur_mission.missioners \
                    if i not in in_game.cur_mission.carry_rec.keys()]

        return Response('OK')
    except Exception as err:
        traceback.print_tb( sys.exc_info()[2] )
        print( type(err) )
        print(err)
        
    
    # for the part we are dealing is the payload part
    try:
        pass
    except:
        pass
    
    return Response('GG')
    
@view_config(route_name='view_hello')
def view_hello(req):
    return Response("<p>Hello</p>")

@view_config(route_name='view_verify')
def view_verify(req):
    if req.params['hub.verify_token'] == 'HKU_dada':
        return Response(req.params['hub.challenge'])
    else:
        return Response('Invalid verify token')