class cards:
    mine = 0
    plant = 1
    tower = 2
    forest = 3
    wastes = 4
    sylvan = 5
    ancient = 6
    expedition = 7
    egg = 8
    relic = 9
    karn = 10

class nodes:
    act = 0
    draw = 1
    look_five = 2
    choose = 3

deck = [4, 4, 4, 3, 3, 4, 4, 4, 8, 2, 20]

class state:
    def __init__(self, prev = None, deck = [], hand = []):
        if prev is None:
            self.node = nodes.act
            self.depth = 0

            self.mana = 0
            self.green = 0
            self.turn = 1
            self.land_plays = 1
            self.tron = False

            self.deck = deck
            self.hand = hand
            self.play = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.tapped = [0, 0, 0, 0, 0]
            self.top = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.bottom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            self.node = nodes.act
            self.depth = prev.depth + 1

            self.mana = prev.mana
            self.green = prev.green
            self.turn = prev.turn
            self.land_plays = prev.land_plays
            self.tron = prev.tron
        
            self.deck = prev.deck.copy()
            self.hand = prev.hand.copy()
            self.play = prev.play.copy()
            self.tapped = prev.tapped.copy()
            self.top = prev.top.copy()
            self.bottom = prev.bottom.copy()

def end(state):
    state.mana = 0
    state.green = 0
    state.turn += 1
    for x, i in state.tapped:
        state.play[i] += x
        state.tapped[i] = 0
    state.node = nodes.draw
    return True

def play_land(state, val):
    if state.land_plays == 0 or state.hand[val] == 0:
        return False
    state.hand[val] -= 1
    state.play[val] += 1
    state.land_plays -= 1
    if state.play[cards.mine] and state.play[cards.plant] and state.play[cards.tower]:
        state.tron = True
    return True

def play_mine(state):
    return state.play_land(cards.mine)

def play_plant(state):
    return state.play_land(cards.plant)

def play_tower(state):
    return state.play_land(cards.tower)

def play_forest(state):
    return state.play_land(cards.forest)

def play_wastes(state):
    return state.play_land(cards.wastes)

def tap_mine(state):
    if state.play[cards.mine] == 0:
        return False
    if(state.tron):
        state.mana += 2
    else:
        state.mana += 1
    state.play[cards.mine] -= 1
    state.tapped[cards.mine] += 1
    return True

def tap_plant(state):
    if state.play[cards.plant] == 0:
        return False
    if(state.tron):
        state.mana += 2
    else:
        state.mana += 1
    state.play[cards.plant] -= 1
    state.tapped[cards.plant] += 1
    return True

def tap_tower(state):
    if state.play[cards.tower] == 0:
        return False
    if(state.tron):
        state.mana += 3
    else:
        state.mana += 1
    state.play[cards.tower] -= 1
    state.tapped[cards.tower] += 1
    return True

def tap_forest(state):
    if state.play[cards.forest] == 0:
        return False
    state.mana += 1
    state.green += 1
    state.play[cards.forest] -= 1
    state.tapped[cards.forest] += 1
    return True

def tap_wastes(state):
    if state.play[cards.wastes] == 0:
        return False
    state.mana += 1
    state.play[cards.wastes] -= 1
    state.tapped[cards.wastes] += 1
    return True

def play_sylvan(state, val):
    if state.mana < 2 or state.green == 0:
        return False
    if state.hand[cards.sylvan] == 0:
        return False
    if state.deck[val] == 0:
        return False
    state.mana -= 2
    state.green -= 1
    if state.green > state.mana:
        state.green = state.mana
    state.hand[cards.sylvan] -= 1
    state.deck[val] -= 1
    state.hand[val] += 1
    for x, i in state.bottom:
        state.deck[i] += x
        state.bottom[i] = 0
    return True

def play_sylvan_mine(state):
    return state.play_sylvan(cards.mine)

def play_sylvan_plant(state):
    return state.play_sylvan(cards.plant)

def play_sylvan_tower(state):
    return state.play_sylvan(cards.tower)

def play_sylvan_forest(state):
    return state.play_sylvan(cards.forest)

def play_ancient(state):
    if state.mana == 0 or state.green == 0:
        return False
    if state.hand[cards.ancient] == 0:
        return False
    state.mana -= 1
    state.green -= 1
    state.hand[cards.ancient] -= 1
    state.node = nodes.look_five
    return True

def play_exped(state):
    if state.mana == 0:
        return False
    if state.hand[cards.expedition] == 0:
        return False
    state.hand[cards.expedition] -= 1
    state.play[cards.expedition] += 1
    state.mana -= 1
    if state.green > state.mana:
        state.green = state.mana
    return True

def play_egg(state):
    if state.mana == 0:
        return False
    if state.hand[cards.egg] == 0:
        return False
    state.hand[cards.egg] -= 1
    state.play[cards.egg] += 1
    state.mana -= 1
    if state.green > state.mana:
        state.green = state.mana
    return True

def play_relic(state):
    if state.mana == 0:
        return False
    if state.hand[cards.relic] == 0:
        return False
    state.hand[cards.relic] -= 1
    state.play[cards.relic] += 1
    state.mana -= 1
    if state.green > state.mana:
        state.green = state.mana
    return True

def crack_exped(state, val):
    if state.mana < 2:
        return False
    if state.play[cards.expedition] == 0:
        return False
    if state.deck[val] == 0:
        return False
    state.play[cards.expedition] -= 1
    state.deck[val] -= 1
    state.hand[val] += 1
    for x, i in state.bottom:
        state.deck[i] += x
        state.bottom[i] = 0
    state.mana -= 2
    if state.green > state.mana:
        state.green = state.mana
    return True

def crack_exped_mine(state):
    return state.crack_exped(cards.mine)
    
def crack_exped_plant(state):
    return state.crack_exped(cards.plant)

def crack_exped_tower(state):
    return state.crack_exped(cards.tower)

def crack_exped_forest(state):
    return state.crack_exped(cards.forest)

def crack_egg(state):
    if state.mana == 0:
        return False
    if state.play[cards.egg] == 0:
        return False
    state.play[cards.egg] -= 1
    state.green += 1
    if state.green > state.mana:
        state.green = state.mana
    state.node = nodes.draw
    return True

def crack_relic(state):
    if state.mana == 0:
        return False
    if state.play[cards.relic] == 0:
        return False
    state.play[cards.relic] -= 1
    state.mana -= 1
    if state.green > state.mana:
        state.green = state.mana
    state.node = nodes.draw
    return True

actions = [
    end,
    play_mine, play_plant, play_tower, play_forest, play_wastes,
    tap_mine, tap_plant, tap_tower, tap_forest, tap_wastes,
    play_sylvan_mine, play_sylvan_plant, play_sylvan_tower, play_sylvan_forest,
    play_ancient,
    play_exped, play_egg, play_relic,
    crack_exped_mine, crack_exped_plant, crack_exped_tower, crack_exped_forest,
    crack_egg, crack_relic
    ]

def choose_ancient(state, val):
    if state.top[val] == 0:
        return False
    state.top[val] -= 1
    state.hand[val] += 1
    for x, i in state.top:
        state.bottom[i] += x
        state.top[i] = 0
    return True

def ancient_mine(state):
    return state.choose_ancient(cards.mine)

def ancient_plant(state):
    return state.choose_ancient(cards.plant)

def ancient_tower(state):
    return state.choose_ancient(cards.tower)

def ancient_forest(state):
    return state.choose_ancient(cards.forest)

def ancient_wastes(state):
    return state.choose_ancient(cards.wastes)

def ancient_exped(state):
    return state.choose_ancient(cards.expedition)

def ancient_egg(state):
    return state.choose_ancient(cards.egg)

def ancient_relic(state):
    return state.choose_ancient(cards.relic)

def ancient_wiff(state):
    for x, i in state.top:
        state.deck[i] += x
        state.top[i] = 0
    return True

choices = [
    ancient_mine, ancient_plant, ancient_tower, ancient_forest, ancient_wastes,
    ancient_exped, ancient_egg, ancient_relic, ancient_wiff
    ]