from pyramid.response import Response
from pyramid.view import view_config
import status
import sending
import moves

ask_to_join = 'Avalon bot game! Please input a # and 6-digit-number to join or create a room (ex. #123456).'

bighead = status.bighead()

@view_config(route_name='view_verify')
def view_verify(req):
    if req.params['hub.verify_token'] == 'HKU_dada':
        return Response(req.params['hub.challenge'])
    else:
        return Response('Invalid verify token')

@view_config(route_name='view_webhook')
def view_webhook(req):
    
    the_id = req.json_body['entry'][0]['messaging'][0]['sender']['id']
    
    # for the part we are dealing is the text part
    try:
        text = req.json_body['entry'][0]['messaging'][0]['message']['text']
        room_num = moves.check_in_room(the_id, bighead)
        if not room_num:
            tt = text[1:]
            if text[0] == '#' and tt.isdigit():
                moves.IntoGame( id, tt, bighead )
            else:
                sending.send_text_message( the_id, ask_to_join )
        else:
            if  bighead.player_table[id].status == 'waiting' and IsRoomHost() and text == 'start':
                bighead.player_table[id].status == 'dark'
                # assign_Character, let some players know each other
                moves.day_dark( bighead.player_table[id], bighead )
            elif bighead.player_table[id].status == 'dark':
                
                # talk shit, players should shut the fk up
            elif bighead.player_table[id].status == 'morning':
                pass
                            
        return Response('OK')
    except:
        pass
    
    # for the part we are dealing is the payload part
    try:
        pass
    except:
        pass
@view_config(route_name='view_hello')
def view_hello(req):
    return Response("<p>Hello</p>")
