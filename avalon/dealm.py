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
    elif payload[0] == 'godness':
        moves.knowing_side(the_id, payload, bighead)
        
def deal_postback(the_id, payload, bighead):
    if payload == '@exp':
        text = 'At the start of every game, players will be randomly assigned to a team. All players will go through a dialog that allows for the minions of Mordred to know who each other are.'
        sending.send_text_message_id( the_id, text )
        text = ' These players will attempt to thwart the servants of Arthur in their attempts to complete quests without giving it away that they are playing for the evil side. If a minion of Mordred manages to get themselves on a quest mission, they can cause it fail.'
        sending.send_text_message_id( the_id, text )
        text = ' Servants of Arthur must use a healthy amount of discussion, accusation, and deduction to determine who is loyal to whom. There are a total of five quests during the game. If Servants of Arthur complete 3 of the 5 quest they win. If the Minions of Mordred can cause 3 of the 5 quests to fail, they win.'
        sending.send_text_message_id( the_id, text )
    elif payload == '@?':
        if (moves.check_in_room(the_id,bighead)):
            text = '[Your current status]\nYou are in room *' + bighead.player_table[ the_id ] + '*\n'
        else:
            text = '[Your current status]\nYou are not in a room. Consider joining one?\n\n'
            text = text + 'Please input a # and 6-digit-number to join or create a room (ex. #123456).'
        sending.send_text_message_id( the_id, text )
    elif payload == '@hurry':
        if moves.check_in_room(the_id,bighead):
            hurry_up(the_id,bighead)
        else:
            text = 'You are missing friends. Join a game first, marginal.'
            sending.send_text_message_id( the_id, text )
    elif payload == '@exit':
        #code to exit room (only available in waiting part)
        in_game = bighead.game_table[ bighead.player_table[ the_id ] ]
        if in_game.status== 'waiting':
            player=in_game.players[the_id]
            sending.send_text_message_id( the_id, "fuck out" )
            in_game.players.pop(the_id)
            bighead.player_table.pop(the_id)
        else:
            sending.send_text_message_id( the_id, "You cannnot exit now" )
            
def hurry_up(the_id,bighead):
    in_game = bighead.game_table[ bighead.player_table[ the_id ] ]
    if in_game.status == 'voting' and in_game.host == the_id:
        [sending.send_vote_choice(i, in_game) for i in in_game.players.keys() \
        if i not in in_game.cur_mission.vote_rec.keys()]
    elif in_game.status == 'conduct' and in_game.host == the_id:
        [sending.send_mission_choice(i, in_game) for i in in_game.cur_mission.missioners \
        if i not in in_game.cur_mission.carry_rec.keys()]
    #add an elif here for other situations requiring a revote (goddess, assassin etc.)
    else:
        text = 'Nothing is missing right now :), Just no one find you (SIGH'
        sending.send_text_message_id( the_id, text )
