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
        self.deck_size = 60

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

    def play_land(self, card):
        if self.land_plays == 0 or self.hand[card] == 0:
            return False
        self.hand[card] -= 1
        self.play[card] += 1
        self.land_plays -= 1
        self.__check_tron()
        return True

    def play_mine(self):
        return self.play_land(mine)

    def play_plant(self):
        return self.play_land(plant)

    def play_tower(self):
        return self.play_land(tower)

    def play_forest(self):
        return self.play_land(forest)

    def play_wastes(self):
        return self.play_land(wastes)

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

    def play_sylvan(self, card):
        if self.mana < 2 or self.green == 0:
            return False
        if self.hand[sylvan] == 0:
            return False
        if self.deck[card] == 0:
            return False
        self.hand[sylvan] -= 1
        self.mana -= 2
        self.green -= 1
        if self.green > self.mana:
            self.green = self.mana
        self.deck[card] -= 1
        self.hand[card] += 1
        self.__shuffle()
        return True

    def play_sylvan_mine(self):
        return self.play_sylvan(mine)

    def play_sylvan_plant(self):
        return self.play_sylvan(plant)

    def play_sylvan_tower(self):
        return self.play_sylvan(tower)

    def play_sylvan_forest(self):
        return self.play_sylvan(forest)

    def play_ancient(self):
        if self.mana == 0 or self.green == 0:
            return False
        if self.hand[ancient] == 0:
            return False
        self.mana -= 1
        self.green -= 1
        self.hand[ancient] -= 1
        pass

    def choose_ancient(self, card):
        if self.top[card] == 0:
            return False
        self.top[card] -= 1
        self.hand[card] += 1
        for x, i in self.top:
            self.bottom[i] += x
            self.top[i] = 0
        return True

    def ancient_mine(self):
        return self.choose_ancient(mine)

    def ancient_plant(self):
        return self.choose_ancient(plant)

    def ancient_tower(self):
        return self.choose_ancient(tower)

    def ancient_forest(self):
        return self.choose_ancient(forest)

    def ancient_wastes(self):
        return self.choose_ancient(wastes)

    def ancient_exped(self):
        return self.choose_ancient(exped)

    def ancient_egg(self):
        return self.choose_ancient(egg)

    def ancient_relic(self):
        return self.choose_ancient(relic)

    def ancient_wiff(self):
        total = 0
        for x, i in self.top:
            total += x
            self.deck[i] += x
            self.top[i] = 0
        if total == 0:
            return False
        return True

    def play_exped(self):
        if self.mana == 0:
            return False
        if self.hand[exped] == 0:
            return False
        self.hand[exped] -= 1
        self.play[exped] += 1
        self.mana -= 1
        if self.green > self.mana:
            self.green = self.mana
        return True

    def play_egg(self):
        if self.mana == 0:
            return False
        if self.hand[egg] == 0:
            return False
        self.hand[egg] -= 1
        self.play[egg] += 1
        self.mana -= 1
        if self.green > self.mana:
            self.green = self.mana
        return True

    def play_relic(self):
        if self.mana == 0:
            return False
        if self.hand[relic] == 0:
            return False
        self.hand[relic] -= 1
        self.play[relic] += 1
        self.mana -= 1
        if self.green > self.mana:
            self.green = self.mana
        return True

    def crack_exped(self, card):
        if self.mana < 2:
            return False
        if self.play[exped] == 0:
            return False
        if self.deck[card] == 0:
            return False
        self.play[exped] -= 1
        self.deck[card] -= 1
        self.hand[card] += 1
        self.mana -= 2
        if self.green > self.mana:
            self.green = self.mana
        return True

    def crack_exped_mine(self):
        return self.crack_exped(mine)
        
    def crack_exped_plant(self):
        return self.crack_exped(plant)

    def crack_exped_tower(self):
        return self.crack_exped(tower)

    def crack_exped_forest(self):
        return self.crack_exped(forest)

    def crack_egg(self):
        if self.mana == 0:
            return False
        if self.play[egg] == 0:
            return False
        self.play[egg] -= 1
        self.green += 1
        if self.green > self.mana:
            self.green = self.mana
        self.__draw()
        return True

    def crack_relic(self):
        if self.mana == 0:
            return False
        if self.play[relic] == 0:
            return False
        self.play[relic] -= 1
        self.mana -= 1
        if self.green > self.mana:
            self.green = self.mana
        self.__draw()
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