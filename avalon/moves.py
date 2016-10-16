from . import status
from . import sending
import random

# bighead.player_table
def check_in_room(the_id,bighead):
    return bighead.player_table.get(the_id, False)
    
# num is the game number
def IntoGame(the_id, num, bighead ,name):
    if bighead.game_table.get(num, False):
        if bighead.game_table[num].status != 'waiting':
            sending.send_text_message_id(the_id,"I am sorry, marginals are not allowed to join now. What a pity!")
            return 0
        
        bighead.game_table[num].add_player(the_id,bighead.player_table,name)
        sending.send_text_message_id(the_id,"Join into the room " + num)
        
    else:
        bighead.new_game( num, the_id, name )
        print( bighead.game_table[num].players[the_id] )
        sending.send_text_message( bighead.game_table[num].players[the_id] ,"Game created. The host can send 'start' to start game, or click 'Let's vote!' to let people check if their votes are sent correctly. :D")
        
    if bighead.game_table[num].getPlayernum() == 10:
        day_dark( bighead.game_table[ num ] )

'''
All three XXX_handler are called by views.py
they expect payload from facebook as an input.
'''

# morning_handler initialize the day
# let the commander to bring people
def morning_handler(the_id, payload, bighead ):
    the_game = bighead.game_table[payload[1]]
    the_game.cur_mission.missioners.append( payload[2] )
    
    num_of_missioners =  len( the_game.cur_mission.missioners )
    missioner_needed =  the_game.Gameset[ the_game.cur_mission_num ]
    if num_of_missioners < missioner_needed:
        available_players = [ i for i in the_game.players.keys() if i not in the_game.cur_mission.missioners ]
        sending.send_people_choice(the_game,available_players)
    else:
        the_game.to_vote()
        print( 'leaving morning handler' )

# When a vote arrive server, voting_hanlder is triggered
def voting_handler( the_id, payload, bighead ):
    print( 'vote getting in m')
    #status.vote_lock.acquire()

    print( 'vote getting received' )
    the_game = bighead.game_table[payload[1]]
    
    if status.use_auto_hurry:
        with the_game.vote_lock:
            # put the arrived vote into record
            the_game.cur_mission.vote_rec[ the_id ] = ( True if payload[2] == 'yes' else False )
            print( the_game.cur_mission.vote_rec )
            print( 'vote releasing in m' )
    else:
        # put the arrived vote into record
        the_game.cur_mission.vote_rec[ the_id ] = ( True if payload[2] == 'yes' else False )
        print( the_game.cur_mission.vote_rec )
        print( 'vote releasing in m' )
    
    # If everyone has voted, then went to mission conduct part
    if len( the_game.cur_mission.vote_rec ) < len( the_game.players ):
        print( 'voting passing' )
        pass
    else:
        text=" "
        for the_id in the_game.cur_mission.vote_rec:
            text=text+ the_game.players[the_id].name+":"+ str(the_game.cur_mission.vote_rec[the_id]) + "\n"
        sending.announce_text_message(the_game, text)
        if the_game.cur_mission.voting_result():
            print( 'vote to conduct' )
            
            sending.announce_text_message(the_game, "Mission Start!!")
            the_game.fail_in_row = 0
            the_game.to_conduct()
        else:
            print( 'vote to morning' )
            sending.announce_text_message(the_game, "The number of \"No\" is outweighting the \"Yes\". \nMission aborted. ")
            if the_game.fail_in_row == bighead.auto_fail_in_row - 1:
                the_game.fail_in_row = 0
                mission_fail(the_game)
            else:
                the_game.fail_in_row += 1
            
            the_game.to_morning()


def conduct_handler(the_id, payload, bighead):
    the_game = bighead.game_table[payload[1]]
    charact=the_game.players[the_id].cha
    
    if charact == "Merlin" or charact == "Royal" or charact == "Percival":
        if payload[2] != 'success' :
            sending.send_text_message( bighead.game_table[ bighead.player_table[the_id] ].players[the_id] , \
                "Fuck you! YOU are a betrayer! 幹！\nI will still submit Success for you. \nNo wonder why people afraid of AI like me going to replace human. \nCuz human got retarded like you.")
        the_game.cur_mission.carry_rec[ the_id ] = True
    else:
        the_game.cur_mission.carry_rec[ the_id ] = ( True if payload[2] == 'success' else False )
    
    if (len(the_game.cur_mission.carry_rec) == len(the_game.cur_mission.missioners)):
        
        if len(the_game.mission_result)==3 and len(the_game.players)>6:
            print("two fail to fail the mission")
            print(len(the_game.mission_result))
            cur_conduct_result=the_game.cur_mission.conduct_result_forth()
        else:
            print( 'into counting part' )
            cur_conduct_result=the_game.cur_mission.conduct_result()

        # mission success
        if cur_conduct_result:
            print("pass")
            mission_success(the_game)
        # mission failed
        else:
            print("fail")
            mission_fail(the_game)
        print("send announce now!")    
        sending.announce_mission_result(
            the_game,
            cur_conduct_result,
            the_game.cur_mission.conduct_success_num(),
            len(the_game.cur_mission.missioners)-the_game.cur_mission.conduct_success_num()
        )
        
        
        if sum(the_game.mission_result)>=3:
            GameOver(payload[1],bighead,True)
        elif len(the_game.mission_result)-sum(the_game.mission_result) >= 3:
            GameOver(payload[1],bighead,False)
        else:
            if len(the_game.mission_result)%2 == 0 and len(the_game.players) > 7:
                print("hey goddess")
                the_game.godness()
            else:
                the_game.to_morning()
        
def knowing_side(the_id, payload, bighead):
    the_game = bighead.game_table[payload[1]]
    pl_list = the_game.players.keys()
    sending.announce_text_message(the_game, "The commander chose to ask for "+ the_game.players[payload[2]].name +"'s identity.")
    charact=the_game.players[payload[2]].cha
    
    if charact == "Merlin" or charact == "Royal" or charact == "Percival":
        sending.send_text_message(the_game.players[the_id],the_game.players[payload[2]].name+" belongs to good guys")
    else:
        sending.send_text_message(the_game.players[the_id],the_game.players[payload[2]].name+" belongs to bad guys")
    the_game.to_morning()
        
def GameOver(game_num,bighead,result):
    the_game = bighead.game_table[game_num]
    pl_list = the_game.players.keys()
    if result:
        sending.announce_text_message(the_game ,"The good guys win,the fucking bad guys still have chance to win only if they can kill merlin")
        
        good_list=["Merlin","Percival","Royal"]
        available_players = [ i for i in pl_list if the_game.players[i].cha in good_list ]
        for pl in pl_list:
            if the_game.players[pl].cha == 'Assassin':
                ass_id=pl
        test="The assassin is "+ the_game.players[ass_id].name +" Now wait for him to choose"
        sending.announce_text_message(the_game ,test)
        print( 'assid '+ass_id )
        print( available_players )
        sending.ass_kill_choice(the_game,ass_id,available_players)
        
    else:
        sending.announce_text_message(the_game ,"The bad guys win,fuck the world")
        for player in pl_list:
            bighead.player_table.pop( player )
        bighead.game_table.pop( game_num )


def assassin_kill(the_id,payload,bighead):
    the_game = bighead.game_table[payload[1]]
    pl_list = the_game.players.keys()
    for pl in pl_list:
            if the_game.players[pl].cha == 'Merlin':
                mer_id=pl
    if payload[2] == mer_id:
        text = "The assasssin chose"+the_game.players[payload[2]].name+ "Holy shit he is right!"
        sending.announce_text_message(the_game ,text)
        sending.announce_text_message(the_game ,"The bad guys win,fuck the world")
    else:
        text = "The assasssin chose "+the_game.players[payload[2]].name+ " BUT merlin is " + the_game.players[mer_id].name
        sending.announce_text_message(the_game ,text)
        sending.announce_text_message(the_game ,"The good guys win,fuck the world")
    for player in pl_list:
        print( 'deleting ' + player )
        bighead.player_table.pop(player)
        
    bighead.game_table.pop( payload[1])
'''
def announce_commander(cmd_idnum):
    text = 'Now choose' + cmd_idnum + ' people to go on the current quest'
    sending.send_text_message_id(cmd_idnum,text)
'''
def mission_success(the_game):
    the_game.mission_result.append(True)
    the_game.cur_mission_num += 1

def mission_fail(the_game):
    the_game.mission_result.append(False)
    the_game.cur_mission_num += 1
    
def day_dark( the_game ):
    '''
    the_game is the Game object.
    day_dark is called after all the people has entered the room.
    The server assign the characters to the players, and let the players knows the needed information.
    then call to_morning to start the mission part.
    '''
    the_game.assign_Character()
    the_game.assign_Gameset()
    text = 'You are '
    # key : all_cha , value : player object
    all_cha = {}
    
    for player in the_game.players.values():
        temp_cha = player.cha
        all_cha[ temp_cha ] = player
        sending.send_text_message( player, text + temp_cha )
    
    player_num = the_game.getPlayernum()
    print(player_num)
    
    t_get_name = lambda cha_name : all_cha[cha_name].name
    shuf_name = lambda name_list : ' and '.join( t_get_name(i) for i in sorted( name_list, key=lambda k: random.random() ) )
   
    '''
    "Merlin Royal Percival Morgana Assassin Royal Oberon Royal Mordred Royal
    '''
    # Merlin
    if player_num < 7:
        text = 'Bad guys are ' + shuf_name([ 'Morgana', 'Assassin'])
    else:
        text = 'Bad guys are ' + shuf_name(['Morgana', 'Assassin', 'Oberon' ])
    sending.send_text_message( all_cha['Merlin'], text )
        
    #Percival
    text = 'Merlin and Morgana are ' + shuf_name(['Morgana', 'Merlin']) + '\nYou must find out and support the real Merlin'
    sending.send_text_message( all_cha['Percival'], text )
        
    # Morgana
    if player_num > 8:
        text = 'Bad guys are ' + shuf_name(['Mordred', 'Assassin'])
    else:
        text = 'Bad guy is ' + t_get_name('Assassin')
    sending.send_text_message( all_cha['Morgana'], text )
    
    # Assassin
    if player_num > 8:
        text = 'Bad guys are ' + shuf_name(['Morgana', 'Mordred'])
    else:
        text = 'Bad guy is ' + t_get_name('Morgana')
    sending.send_text_message( all_cha['Assassin'], text )
    
    #Mordred
    if player_num > 8:
        text = 'Bad guys are ' + shuf_name(['Mordred', 'Assassin'])
        sending.send_text_message( all_cha['Mordred'], text )
    
    the_game.to_morning()
    return True