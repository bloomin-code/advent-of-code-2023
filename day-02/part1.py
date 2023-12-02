from collections import namedtuple, defaultdict

Round = namedtuple("Round", ['red', 'green', 'blue'])

Game = namedtuple("Game", ['id', 'rounds'])

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def main():
    games = []
    with open('input.txt') as f:
        for line in f:
            game_id, rounds = line.strip().split(': ')
            game = Game(int(game_id.strip('Game ')), [])

            for round in rounds.split('; '):
                round_info = defaultdict(int)
                for item in round.split(', '):
                    cubes, color = item.split(' ')
                    round_info[color] += int(cubes)
                game.rounds.append(Round(round_info['red'], round_info['green'], round_info['blue']))
            games.append(game)
    # The Elf would first like to know which games would have been possible
    # if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
    total = 0
    for game in games:
        for round in game.rounds:
            if round.red > MAX_RED or round.green > MAX_GREEN or round.blue > MAX_BLUE:
                break
        else:
            total += game.id
    print('part 1:', total)

if __name__ == '__main__':
    main()
