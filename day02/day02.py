import sys
from functools import reduce
from operator import mul

def are_valid_cubes(cubes):
    max_cubes = {'red': 12, 'green': 13, 'blue': 14}
    cube_list = [cube.strip() for cube in cubes.split(',')]
    for cube in cube_list:
        count, color = cube.split(' ')
        if max_cubes[color] < int(count):
            return False 
    
    return True

def is_valid_game(game):
    return all(are_valid_cubes(cubes) for cubes in game.split(';'))
        
def get_valid_sum(games):
    valid_sum = 0
    for game_pair in games:
        game_id, game = game_pair.split(':')
        if is_valid_game(game):
            valid_sum += int(game_id.split(' ')[1])

    return valid_sum

def get_power(game):
    max_count = {'red': 0, 'green': 0, 'blue': 0}
    draws = game.split(';')

    for draw in draws:
        cube_list = [cube.strip() for cube in draw.split(',')]
        for cube in cube_list:
            count, color = cube.split(' ')
            max_count[color] = max(max_count[color], int(count))
    
    return reduce(mul, max_count.values())
        
def get_total_power(games):
    total_power= 0
    for game_pair in games:
        _, game = game_pair.split(':')
        total_power += get_power(game)

    return total_power

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    print(get_valid_sum(lines))
    print(get_total_power(lines))

if __name__ == '__main__':
    main()
