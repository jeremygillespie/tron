class cards:
    mine = 0
    plant = 1
    tower = 2
    forest = 3
    wastes = 4
    exped = 5
    egg = 6
    relic = 7
    sylvan = 8
    ancient = 9
    karn = 10

deck = [4, 4, 4, 3, 3, 4, 4, 4, 8, 2, 20]

class state:
    def __init__(self, prev = None, deck = [], hand = []):
        if prev is None:
            self.depth = 0

            self.deck = deck
            self.hand = hand
            self.deck_size = 0
            for x in self.deck:
                self.deck_size += x

            self.mana = 0
            self.green = 0
            self.turn = 1
            self.land_played = False
            self.tron = False
            self.play = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.tapped = [0, 0, 0, 0, 0]

            self.anceint_played = False
            self.ancient_tried = [False, False, False, False, False, False, False, False]
        else:
            self.depth = prev.depth + 1

            self.deck = prev.deck.copy()
            self.hand = prev.hand.copy()
            self.play = prev.play.copy()
            self.tapped = prev.tapped.copy()

            self.mana = prev.mana
            self.green = prev.green
            self.turn = prev.turn
            self.land_plays = prev.land_plays
            self.tron = prev.tron
            self.deck_size = prev.deck_size

            self.anceint_played = prev.anceint_played
            self.ancient_tried = prev.ancient_tried.copy()

def draw(prev):
    if prev.deck_size == 0:
        return [], []
    successors = []
    weights = []
    for x, i in prev.deck:
        if x > 0:
            new = state(prev)
            new.deck_size -= 1
            new.deck[i] -= 1
            new.hand[i] += 1
            successors.append(new)
            weights.append(x)
    return successors, weights

def end(prev):
    new = state(prev)
    new.mana = 0
    new.green = 0
    new.turn += 1
    for y, j in new.tapped:
        new.play[j] += y
        new.tapped[j] = 0
    return draw(new)

def play_land(prev, val):
    if prev.land_plays == 0 or prev.hand[val] == 0:
        return [], []
    new = state(prev)
    new.hand[val] -= 1
    new.play[val] += 1
    new.land_played = True
    if new.play[cards.mine] and new.play[cards.plant] and new.play[cards.tower]:
        new.tron = True
    return [new], [1.0]

def play_mine(prev):
    return play_land(prev, cards.mine)

def play_plant(prev):
    return play_land(prev, cards.plant)

def play_tower(prev):
    return play_land(prev, cards.tower)

def play_forest(prev):
    return play_land(prev, cards.forest)

def play_wastes(prev):
    return play_land(prev, cards.wastes)

def tap_mine(prev):
    if prev.play[cards.mine] == 0:
        return [], []
    new = state(prev)
    if(new.tron):
        new.mana += 2
    else:
        new.mana += 1
    new.play[cards.mine] -= 1
    new.tapped[cards.mine] += 1
    return [new], [1.0]

def tap_plant(prev):
    if prev.play[cards.plant] == 0:
        return [], []
    new = state(prev)
    if(new.tron):
        new.mana += 2
    else:
        new.mana += 1
    new.play[cards.plant] -= 1
    new.tapped[cards.plant] += 1
    return [new], [1.0]

def tap_tower(prev):
    if prev.play[cards.tower] == 0:
        return [], []
    new = state(prev)
    if(new.tron):
        new.mana += 3
    else:
        new.mana += 1
    new.play[cards.tower] -= 1
    new.tapped[cards.tower] += 1
    return [new], [1.0]

def tap_forest(prev):
    if prev.play[cards.forest] == 0:
        return [], []
    new = state(prev)
    new.mana += 1
    new.green += 1
    new.play[cards.forest] -= 1
    new.tapped[cards.forest] += 1
    return [new], [1.0]

def tap_wastes(prev):
    if prev.play[cards.wastes] == 0:
        return [], []
    new = state(prev)
    new.mana += 1
    new.play[cards.wastes] -= 1
    new.tapped[cards.wastes] += 1
    return [new], [1.0]

def play_sylvan(prev, val):
    if prev.mana < 2 or prev.green == 0:
        return [], []
    if prev.hand[cards.sylvan] == 0:
        return [], []
    if prev.deck[val] == 0:
        return [], []
    new = state(prev)
    new.mana -= 2
    new.green -= 1
    if new.green > new.mana:
        new.green = new.mana
    new.hand[cards.sylvan] -= 1
    new.deck[val] -= 1
    new.hand[val] += 1
    return [new], [1.0]

def sylvan_mine(prev):
    return play_sylvan(prev, cards.mine)

def sylvan_plant(prev):
    return play_sylvan(prev, cards.plant)

def sylvan_tower(prev):
    return play_sylvan(prev, cards.tower)

def sylvan_forest(prev):
    return play_sylvan(prev, cards.forest)

def play_ancient(prev):
    if prev.mana == 0 or prev.green == 0:
        return [], []
    if prev.hand[cards.ancient] == 0:
        return [], []
    new = state(prev)
    new.mana -= 1
    new.green -= 1
    new.hand[cards.ancient] -= 1
    new.anceint_played = True
    return [new], [1.0]

def play_exped(prev):
    if prev.mana == 0:
        return [], []
    if prev.hand[cards.exped] == 0:
        return [], []
    new = state(prev)
    new.hand[cards.exped] -= 1
    new.play[cards.exped] += 1
    new.mana -= 1
    if new.green > new.mana:
        new.green = new.mana
    return [new], [1.0]

def play_egg(prev):
    if prev.mana == 0:
        return [], []
    if prev.hand[cards.egg] == 0:
        return [], []
    new = state(prev)
    new.hand[cards.egg] -= 1
    new.play[cards.egg] += 1
    new.mana -= 1
    if new.green > new.mana:
        new.green = new.mana
    return [new], [1.0]

def play_relic(prev):
    if prev.mana == 0:
        return [], []
    if prev.hand[cards.relic] == 0:
        return [], []
    new = state(prev)
    new.hand[cards.relic] -= 1
    new.play[cards.relic] += 1
    new.mana -= 1
    if new.green > new.mana:
        new.green = new.mana
    return [new], [1.0]

def crack_exped(prev, val):
    if prev.mana < 2:
        return [], []
    if prev.play[cards.exped] == 0:
        return [], []
    if prev.deck[val] == 0:
        return [], []
    new = state(prev)
    new.play[cards.exped] -= 1
    new.deck[val] -= 1
    new.hand[val] += 1
    new.mana -= 2
    if new.green > new.mana:
        new.green = new.mana
    return [new], [1.0]

def crack_exped_mine(prev):
    return crack_exped(prev, cards.mine)
    
def crack_exped_plant(prev):
    return crack_exped(prev, cards.plant)

def crack_exped_tower(prev):
    return crack_exped(prev, cards.tower)

def crack_exped_forest(prev):
    return crack_exped(prev, cards.forest)

def crack_egg(prev):
    if prev.mana == 0:
        return [], []
    if prev.play[cards.egg] == 0:
        return [], []
    new = state(prev)
    new.play[cards.egg] -= 1
    new.green += 1
    if new.green > new.mana:
        new.green = new.mana
    return draw(new)

def crack_relic(prev):
    if prev.mana == 0:
        return [], []
    if prev.play[cards.relic] == 0:
        return [], []
    new = state(prev)
    new.play[cards.relic] -= 1
    new.mana -= 1
    if new.green > new.mana:
        new.green = new.mana
    return draw(new)

actions = [
    end,
    play_mine, play_plant, play_tower, play_forest, play_wastes,
    tap_mine, tap_plant, tap_tower, tap_forest, tap_wastes,
    sylvan_mine, sylvan_plant, sylvan_tower, sylvan_forest,
    play_exped, play_egg, play_relic,
    crack_exped_mine, crack_exped_plant, crack_exped_tower, crack_exped_forest,
    crack_egg, crack_relic
    ]

def choose_ancient(prev, val):
    if prev.anceint_tried[val]:
        return [], []
    success = state(prev)
    success.deck[val] -= 1
    success.hand[val] += 1
    success.ancient_tried = [False, False, False, False, False, False, False, False]
    success.anceint_played = False

    failure = state(prev)
    failure.ancient_tried[val] = True

    prob = 1.0 #TODO what is the probability of finding what you want?

    return [success, failure], [prob, 1.0 - prob]

def ancient_mine(prev):
    return choose_ancient(prev, cards.mine)

def ancient_plant(prev):
    return choose_ancient(prev, cards.plant)

def ancient_tower(prev):
    return choose_ancient(prev, cards.tower)

def ancient_forest(prev):
    return choose_ancient(prev, cards.forest)

def ancient_wastes(prev):
    return choose_ancient(prev, cards.wastes)

def ancient_exped(prev):
    return choose_ancient(prev, cards.exped)

def ancient_egg(prev):
    return choose_ancient(prev, cards.egg)

def ancient_relic(prev):
    return choose_ancient(prev, cards.relic)

def ancient_wiff(prev):
    return [prev], [1.0]

choices = [
    ancient_mine, ancient_plant, ancient_tower, ancient_forest, ancient_wastes,
    ancient_exped, ancient_egg, ancient_relic, ancient_wiff
    ]