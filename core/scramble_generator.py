import random

def generate_scramble(length=20):
    moves = ["U", "D", "L", "R", "F", "B"]
    modifiers = ["", "'", "2"]
    scramble = []
    previous = ""

    while len(scramble) < length:
        move = random.choice(moves)
        if move == previous:
            continue
        previous = move
        scramble.append(move + random.choice(modifiers))

    return ' '.join(scramble)
