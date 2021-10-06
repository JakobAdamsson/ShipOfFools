import random

class Die():
    """
    Denna klass hanterar skapendet av tärningar samt håller reda på vardera tärnings värde som genereras
    från funktionen roll där jag hämtar ett slumpmässigt värde mellan 1-6 m.h.a att impotera random
    """
      
    def __init__(self, _value = None):
        self._value = _value
        self.roll() #vid varje instans av klassen körs roll funktionenn
    
    def get_value(self):
        return self._value'
    
    def roll(self):
        self._value = random.randint(1, 6)
        return self._value

class DiceCup():
    """
    Denna klassen ska sköta koppen där tärningarna ligger i, den ska kunna visa vilka värden tärningarna har,
    den ska kunna visa om en tärning är låst eller ej samt kunna släppa tärning/tärningar om de är låsta
    """
    
    def __init__(self, dice_amount = 5):
        self.dice_amount = dice_amount #Tärningar
        self._dice_list = [Die() for _ in range(self.dice_amount)] #skapar ett godtyckligt antal tärningar och placerar dom i denna list
        self._locked_values = [False for _ in range (self.dice_amount)] #skapar exakt lika många false values som det finns tärningar
        
    def roll(self):   
        for i,x in enumerate(self._dice_list):   
            if self._locked_values[i] == False:
                self._dice_list[i].roll()
        
    def occupied_values(self):    
        for x,y in enumerate(self._dice_list):
            if self._locked_values[x] == False:
                print(f'T{x+1}. {y.get_value()}')
            else:
                print(f'T{x+1}. {y.get_value()} - BANKED')
                       
    def release_all(self):
        for index, bool_value in enumerate(self._locked_values):
            self._locked_values[index] = False
            self._dice_list[index].roll()

    def release(self, index: int):
        self._locked_values[index-1] = False
        self._dice_list[index-1].roll()
                   
    def die_value(self):
        for i in range(self.dice_amount):
            self._dice_list[i].get_value()

    def bank(self, index):
        #print(f'{index} bankad')
        self._locked_values[index] = True
    
    def is_banked(self, index: int):
        return self._locked_values[index-1]
       

class ShipOfFoolsGame():
    def __init__(self):
        self._cup = DiceCup(5)
        self._winning_score = 50
        self._scm = [] #ship index 0, captain index 1, mate index 2
        self.has_ship = False
        self.has_captain = False
        self.has_mate = False
        
    def reset(self): 
        """"""
        self._cup.release_all()
        self.has_ship = False
        self.has_captain = False
        self.has_mate = False 

    def turn(self):
        """Hanterar spellogiken i spelet samt kallar på funktionen crew som presenterar resultatet"""
        crew = 0
        print('----------')
        self.reset()
        for i in range(3):
            self._cup.roll()
            for index, value in enumerate(self._cup._dice_list):
                if value.get_value() == 6 and self.has_ship == False:
                    self._cup.bank(index)
                    self.has_ship = True
                
            for index, value in enumerate(self._cup._dice_list):
                if value.get_value() == 5 and self.has_ship == True and self.has_captain == False:
                    self._cup.bank(index)
                    self.has_captain = True
            
            for index, value in enumerate(self._cup._dice_list):
                if value.get_value() == 4 and self.has_ship == True and self.has_captain == True and self.has_mate == False:
                    self._cup.bank(index)
                    self.has_mate = True
        
            if self.has_captain == True and self.has_ship == True and self.has_mate == True:
                for index, value in enumerate(self._cup._dice_list):
                    if value.get_value() > 3 and self._cup._locked_values[index] == False:
                        self._cup.bank(index)
                for i, s in enumerate(self._cup._dice_list):
                    crew += s.get_value()
                crew = crew - 15
     
            self._cup.occupied_values()
        return crew
                  
class Player():
    """Klass som hanterar skapandet av spelare där namn och vilket score den har"""
    
    def __init__(self, _name:str):
        self._name = _name
        self._score = 0
    
    def display_name(self):
        return self._name
    
    def current_score(self):
        return self._score

    def reset_score(self):
        self._score = 0
    
    def play_turn(self, game): #crew_Value hämtar sitt värde från play_round i playroom klassen
        print(f'{self._name} rullar')
        game.turn()
        self._score += game.turn() #rättat

class PlayRoom():
    def __init__(self):
        self._game = None
        self._players = [] #använder en lista då de kan vara fler än 1 vinnare
        self._winner = []
    
    def add_player(self):
        self._players = [Player(input('Namn: ')) for _ in range(2)]

    def set_game(self):
        self._game = ShipOfFoolsGame()
        
    def reset_scores(self):
        for i in self._players:
            i.reset_score()  
    
    def play_round(self):
        for player in self._players:
            player.play_turn(self._game) #rättat

    def game_finished(self):
        """Hanterar när spelet ska avslutas eller inte, denna funktion kommer köras tills winner_found retunerar True

        Returns:
            Bool: Retunerar False tills en spelrae uppnått poängen
        """
        winner_found = False
        for player in self._players:
            print(f'{player.display_name()} -> {player.current_score()} ')
            if player.current_score() >= self._game._winning_score:
                self._winner.append(player)
                winner_found = True
        return winner_found
        
    def print_winner(self):
        for i in self._winner:
            print('\nOCH VINNAREN ÄR DUNDUNDUNDUN.....')
            print(f'{i.display_name()} som lyckades slå hela {i.current_score()} poäng woooowowowowooww')
            
if __name__ == '__main__':
    room = PlayRoom()
    room.add_player()
    room.set_game()
    while not room.game_finished():
        room.play_round()
    room.print_winner()
