imp

class bighead():
    def __init__(self):
        self.player_table = {}
        self.game_table = {}
    
    def new_game(self, num):
        self.game_table[str(num)] = Game(str(num))
        
        
class Game():
    def __init__(self, num):
        self.num = num
        self.players = []
        
    def add_player(self,id,table):
        newPlayer=player(id)
        table[id]=self.num
    
    def assign_Character(num):
        for i in range(1:num):
            a
        
        
        
class player():
    def __init__(self, id):
        self.id = id
    
    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
    
    
    def getCharacter(self):
        return self._cha

    def setCharacter(self, cha):
        self._cha = cha
        
    # cha must be a string 
    cha = property(getCharacter, setCharacter)
    name=property(getName,setName)
    


Character_list={
    "Merlin":[0],
    "Rubbish"
    ""
    
}