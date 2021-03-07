mine = 0
plant = 1
tower = 2
forest = 3
wastes = 4
sylvan = 5
ancient = 6
exped = 7
egg = 8
relic = 9
karn = 10

deck = [4, 4, 4, 3, 3, 4, 4, 4, 8, 2, 20]

class state:
    def __init__(self, prev = None):
        self.mana = 0
        self.green = 0
        self.turn = 1
        self.land_plays = 1
        self.tron = False
        self.deck = deck
        self.top = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.bottom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.play = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tapped = [0, 0, 0, 0, 0]

    def __draw(self):
        pass

    def __shuffle(self):
        for x, i in self.bottom:
            self.deck[i] += x
            self.bottom[i] = 0

    def __ancient_done(self):
        for x, i in self.top:
            self.bottom[i] += x
            self.top[i] = 0

    def __check_tron(self):
        if self.play[mine] and self.play[plant] and self.play[tower]:
            self.tron = True

    def end(self):
        self.mana = 0
        self.green = 0
        self.turn += 1
        for x, i in self.tapped:
            self.play[i] += x
            self.tapped[i] = 0
        self.__draw()

    def play_mine(self):
        if self.land_plays == 0 or self.hand[mine] == 0:
            return False
        self.hand[mine] -= 1
        self.play[mine] += 1
        self.land_plays -= 1
        self.__check_tron()
        return True

    def play_plant(self):
        if self.land_plays == 0 or self.hand[plant] == 0:
            return False
        self.hand[plant] -= 1
        self.play[plant] += 1
        self.land_plays -= 1
        return True

    def play_tower(self):
        if self.land_plays == 0 or self.hand[tower] == 0:
            return False
        self.hand[tower] -= 1
        self.play[tower] += 1
        self.land_plays -= 1
        self.__check_tron()
        return True

    def play_forest(self):
        if self.land_plays == 0 or self.hand[forest] == 0:
            return False
        self.hand[forest] -= 1
        self.play[forest] += 1
        self.land_plays -= 1
        return True

    def play_wastes(self):
        if self.land_plays == 0 or self.hand[wastes] == 0:
            return False
        self.hand[wastes] -= 1
        self.play[wastes] += 1
        self.land_plays -= 1
        return True

    def tap_mine(self):
        if self.play[mine] == 0:
            return False
        if(self.tron):
            self.mana += 2
        else:
            self.mana += 1
        self.play[mine] -= 1
        self.tapped[mine] += 1
        return True

    def tap_plant(self):
        if self.play[plant] == 0:
            return False
        if(self.tron):
            self.mana += 2
        else:
            self.mana += 1
        self.play[plant] -= 1
        self.tapped[plant] += 1
        return True

    def tap_tower(self):
        if self.play[tower] == 0:
            return False
        if(self.tron):
            self.mana += 3
        else:
            self.mana -= 1
        self.play[tower] -= 1
        self.tapped[tower] += 1
        return True

    def tap_forest(self):
        if self.play[forest] == 0:
            return False
        self.mana += 1
        self.green += 1
        self.play[forest] -= 1
        self.tapped[forest] += 1
        return True

    def tap_wastes(self):
        if self.play[wastes] == 0:
            return False
        self.mana += 1
        self.play[wastes] -= 1
        self.tapped[wastes] += 1
        return True

    def play_sylvan_mine(self):
        if self.deck[mine] == 0:
            return False
        self.deck[mine] -= 1
        self.hand[mine] += 1
        self.__shuffle()
        return True

    def play_sylvan_plant(self):
        if self.deck[plant] == 0:
            return False
        self.deck[plant] -= 1
        self.hand[plant] += 1
        self.__shuffle()
        return True

    def play_sylvan_tower(self):
        if self.deck[tower] == 0:
            return False
        self.deck[tower] -= 1
        self.hand[tower] += 1
        self.__shuffle()
        return True

    def play_sylvan_forest(self):
        if self.deck[forest] == 0:
            return False
        self.deck[forest] -= 1
        self.deck[forest] += 1
        self.__shuffle()
        return True

    actions = [
        end,
        play_mine, play_plant, play_tower, play_forest, play_wastes,
        tap_mine, tap_plant, tap_tower, tap_forest, tap_wastes,
        play_sylvan_mine, play_sylvan_plant, play_sylvan_tower, play_sylvan_forest,
        play_ancient,
        ancient_mine, ancient_plant, ancient_tower, ancient_forest, ancient_wastes,
        ancient_exped, ancient_egg, ancient_relic, ancient_wiff,
        play_exped, play_egg, play_relic,
        crack_exped_mine, crack_exped_plant, crack_exped_tower, crack_exped_forest,
        crack_egg, crack_relic
        ]