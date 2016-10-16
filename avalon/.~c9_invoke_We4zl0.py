from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):
    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'The second button...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = '[Your current status]\nYou '
            text = '[Your current status]\nYou are in room *' + bighead.player_table[ the_id ] + '*\n'
        else:
            text = '[Your current status]\nYou are not in a room. Consider joining one?\n\n'
            text = text + 'Please input a # and 6-digit-number to join or create a room (ex. #123456).'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'The fourth button...'
        sending.send_text_message( the_id, text )

'''        
from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )from . import moves
from . import sending

def is_echo(req):
    try:
        req.json_body['entry'][0]['messaging'][0]['message']['is_echo']
        print('deal echo')
        return True
    except:
        return False
        
def deal_playload(the_id, payload, bighead):
    payload = payload.split('-')
    if payload[0] == 'sendppl':
        moves.morning_handler( the_id, payload, bighead )
    elif payload[0] == 'voting':
        moves.voting_handler( the_id, payload, bighead )
    elif payload[0] == 'mission':
        moves.conduct_handler( the_id, payload, bighead )
    elif payload[0] == 'asskill':
        moves.assassin_kill(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):

    if payload == '@exp':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@switch':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@?':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
    elif payload == '@hurry':
        text = 'Explain game rules...'
        sending.send_text_message( the_id, text )
'''