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
    total = 0
    for game in games:
        min_req_cubes = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }
        for round in game.rounds:
            min_req_cubes['red'] = max(min_req_cubes['red'], round.red)
            min_req_cubes['green'] = max(min_req_cubes['green'], round.green)
            min_req_cubes['blue'] = max(min_req_cubes['blue'], round.blue)
        total += min_req_cubes['red'] * min_req_cubes['green'] * min_req_cubes['blue']
    print('part 2:', total)

if __name__ == '__main__':
    main()
