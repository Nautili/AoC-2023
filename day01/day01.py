import sys

def get_value(s):
    numbers = [int(c) for c in s if c.isdigit()]
    return numbers[0] * 10 + numbers[-1]

def get_sum(lines):
    return sum(get_value(line) for line in lines)

def map_number_words(line):
    number_map = {
        "one": 'o1e',
        "two": 't2o',
        "three": 't3e',
        "four": '4',
        "five": '5e',
        "six": '6',
        "seven": '7n',
        "eight": 'e8t',
        "nine": 'n9e'}
    
    for word, number in number_map.items():
        line = line.replace(word, number)
    return line

def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    #part 1
    #print(get_sum(lines))

    cleaned_lines = [map_number_words(line) for line in lines]
    print(get_sum(cleaned_lines))


if __name__ == '__main__':
    main()
