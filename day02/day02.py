import sys
from functools import reduce
from operator import mul

def are_valid_cubes(cubes):
    max_cubes = {'red': 12, 'green': 13, 'blue': 14}
    return all(max_cubes[color] >= int(count) for count, color in cubes)

def is_valid_game(game):
    return all(are_valid_cubes(cubes) for cubes in game)
        
def get_valid_sum(games):
    return sum(game.game_id for game in games if is_valid_game(game.draws))

def get_power(game):
    max_count = {'red': 0, 'green': 0, 'blue': 0}
    for draw in game.draws:
        for count, color in draw:
            max_count[color] = max(max_count[color], int(count))
    
    return reduce(mul, max_count.values())
        
def get_total_power(games):
    return sum(get_power(game) for game in games)


class Game:
    def __init__(self, game_id, draws):
        self.game_id = game_id
        self.draws = draws

def parse_games(games):
    parsed_games = []
    for game_pair in games:
        game_id, game = game_pair.split(':')
       
        parsed_draws = []
        draws = game.split(';')     
        for draw in draws:
            cube_list = [cube.strip() for cube in draw.split(',')]
            parsed_cubes = []
            for cube in cube_list:
                count, color = cube.split(' ')
                parsed_cubes.append((int(count), color))
            parsed_draws.append(parsed_cubes)
        parsed_games.append(Game(int(game_id.split(' ')[1]), parsed_draws))

    return parsed_games


def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]
    
    games = parse_games(lines)

    print(get_valid_sum(games))
    print(get_total_power(games))

if __name__ == '__main__':
    main()
