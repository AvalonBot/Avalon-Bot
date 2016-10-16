import time
import random
import threading
import multiprocessing
from . import sending
from collections import deque

Character_list=["Merlin","Assassin","Percival","Morgana","Royal","Royal","Oberon","Royal","Mordred","Royal"]

hurry_interval = 10

use_auto_hurry = True

GameSet_list = {
    4 : [1,1,1,1,1],
    5 : [2,3,2,3,3],
    6 : [2,3,4,3,4],
    7 : [2,3,3,4,4],
    8 : [3,4,4,5,5],
    9 : [3,4,4,5,5],
    10 : [3,4,4,5,5]
}

try:
    vote_lock.release()
    print( 'release not right...' )
except:
    print( 'lock is ok' )
    pass
    
class Bighead():
    def __init__(self):
        # key : player_id , value : game_num
        self.player_table = {}
        # key : game_num , value : game object
        self.game_table = {}
        # When voting fail exceeds following times, the mission fail automatically.
        self.auto_fail_in_row = 5

    # num is Game_num, id is the host id
    def new_game(self, num, the_id, name):
        self.game_table[ num ] = Game( num, the_id, name)
        self.player_table[ the_id ] = num
        
class Game():
    #Constructor for creating a room
    # player_order is for know who is next commander
    def __init__(self, Game_num, the_id, name):
        assert isinstance( Game_num, str )
        self.Game_num = Game_num
        # key : player_id , value : player object
        self.players = {the_id : player(the_id, name)}
        self.status = 'waiting'
        self.host = the_id
        self.commander=self.host
        self.player_order = [the_id] # For the commander order
        
        self.cur_mission = None
        self.past_missions = []
        
        self.cur_mission_num = 0
        self.mission_result = []  # true/false of each mission
        
        self.fail_in_row = 0 # if fail_in_row reach 5, the mission fail automatically.
        
        # For the auto-hurry function, Stop voting_handler and vote_hurry performing together.
        # Lock would be acquire by vote_hurry and moves.voting _handler
        self.vote_lock = threading.Lock()
        
    def check_enough(self):
        return (True if len(self.players) > 3 else False)
    
    #add a player to the game, table is the player_table in bighead 
    def add_player(self,the_id,table,name):
        table[the_id]=self.Game_num
        self.players[the_id] = player( the_id, name)
        self.player_order.append( the_id )
        text = self.players[the_id].name + ' enter the game, there are ' + str(len(self.players)) + ' people now'
        sending.announce_text_message( self, text )
    
    #assign game characters to the players
    def assign_Character(self):
        cur_charact = Character_list[ 0:len(self.players) ]
        random.shuffle(cur_charact)
        for player, chara in zip( self.players.values() ,cur_charact ):
            player.cha = chara
    
    def assign_Gameset(self):
        self.Gameset = GameSet_list[ len(self.players) ]
    
    def getPlayernum(self):
        return len(self.players)
        
    # please use this instead of using setCommander and morning directly
    def to_morning(self):
        
        if self.cur_mission:
            temp_m_id =  self.cur_mission.the_id + 1
            self.past_missions.append( self.cur_mission )
        else:
            temp_m_id = 0
            
        self.setCommander()
   #     print('in morning + ' + self.commander)
        self.cur_mission = Mission(self.commander, temp_m_id)
        
        self.status = 'morning'
        sending.send_people_choice( self, self.players.keys() )
    
    def to_vote(self):
        print( 'in the to_vote' )
        self.status='voting'
        sending.announce_missioners(self)
        sending.send_vote_choice_all(self)
        if use_auto_hurry:
            self.vote_hurry_thread(self.cur_mission.the_id)
        
        print('leaving to vote')
        
# -----------VVVVVV auto hurry  VVVVVV----------------------------
    def vote_hurry_thread(self, mis_id ):
        p = threading.Thread( target=self.vote_hurry, args=(mis_id) )
        p.start()
        print('leaving')
    
    def vote_hurry(self, mis_id):
        time.sleep(hurry_interval)
        print('hurrying')
        print('getting lockkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        self.vote_lock.acquire()
        print('lock acr')
        if self.cur_mission.the_id == mis_id:
            all_s = 0
            for i in self.players.keys():
                if i not in self.cur_mission.vote_rec.keys():
                    all_s += 1 
                    sending.send_vote_choice(i, self)
            print('lock release')
            self.vote_lock.release()
            
            # if anyone has not voted, schedule next hurry
            if all_s > 0:
                print( 'scheduling nxt' )
                self.vote_hurry(mis_id, self)
        else:
            print( 'Mission Obselete !!\nMission num : ' + mis_id )
            vote_lock.release()
        
        print('leaving hurry')

# -----------^^^^^^^^^ auto hurry  ^^^^^^^^^^^----------------------------

    def to_conduct(self):
        self.status="conduct"
        print('get into conduct status')
        sending.send_mission_choice_all(self)
        
    def godness(self):
        text="The commander meet the Godness. You may ask 1 person to tell you his side"
        sending.godness_choice(self,self.cur_mission.commander, self.players.keys())
        
    def setCommander(self):
        queue = self.player_order
        if queue.index(self.commander)==len(queue)-1:
            self.commander=queue[0]
        else:
            self.commander = queue[queue.index(self.commander)+1]
            
        #announce Mission Number and missioners needed
        text = "Mission " + str(self.cur_mission_num + 1) + "\n"+ str(self.Gameset[self.cur_mission_num])+" missioners are needed."
        if len(self.mission_result)==3 and len(self.players)>6:
            text = text + "\nIn this mission, you will need 2 failure in order to fail the mission."
        if self.fail_in_row != 0:
            text = text + "\n(This mission has been aborted for "+str(self.fail_in_row)+" times. Mission will fail if 5 times achieved)"
        
        text =text + "\n\nThis time the commander is " + self.players[self.commander].name
        sending.announce_text_message( self, text)
        
class Mission():
    def __init__(self, cmder, the_id):
        self.missioners = []
        self.commander = cmder
        self.vote_rec = {}
        self.carry_rec = {}
        self.the_id = the_id
        
    def add_missioner(self, ppl_id):
        self.missioners.append(ppl_id)
        
    def vote(self, ppl_id, res):
        assert isinstance( res, bool )
        self.vote_rec[ppl_id] = res
        
    def carry(self, ppl_id, res):
        assert isinstance( res, bool )
        self.carry_rec[ppl_id] = res
    
    def voting_result(self): 
        return True if sum( self.vote_rec.values() ) > len(self.vote_rec)/2 else False
    
    def conduct_result( self ): 
        return True if all( self.carry_rec.values() ) else False
    
    def conduct_result_forth( self ):
        return True if sum( self.carry_rec.values() ) > len( self.carry_rec )-2 else False
    
    def conduct_success_num( self ):
        return sum(self.carry_rec.values())
    
class player():
    def __init__(self, the_id, name):
        self.id = the_id
        self.name = name
        self.cha = None
        self.text_deque = deque()
        self.text_lock = threading.Lock()

'''
Progress_list=["Wait","Assign"]
game status:
    waiting : waiting for ppl to join game
    dark : after assigning character, tell each character the info they should know about each other
    morning : 
    voting : 
    conduct : 
'''