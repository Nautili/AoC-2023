import sys

def get_count_parts(map):
    total_count = 0
    for row in range(1, len(map) - 1):
        cur_num = 0
        is_part = False
        for col in range(1, len(map[row]) - 1):
            if map[row][col].isdigit():
                cur_num = cur_num * 10 + int(map[row][col])
                for check_row in range(row - 1, row + 2):
                    for check_col in range(col - 1, col + 2):
                        if not map[check_row][check_col].isdigit() \
                           and not map[check_row][check_col] == '.':
                            is_part = True
            else:
                if is_part:
                    total_count += cur_num
                cur_num = 0
                is_part = False
        if is_part:
            total_count += cur_num
    return total_count

def extract_number(map, row, col, numbers):
    cur_num = 0
    while map[row][col].isdigit():
        cur_num = cur_num * 10 + int(map[row][col])
        col += 1
    if cur_num > 0:
        numbers.append(cur_num)

    return col

def get_row_numbers(map, row, col):
    base_col = col
    numbers = []
    while map[row][col].isdigit():
        col -= 1

    col = extract_number(map, row, col + 1, numbers)
    while col < base_col + 2 and not map[row][col].isdigit():
        col += 1
    extract_number(map, row, col, numbers)

    return numbers

def get_ratio(map, row, col):
    numbers = []
    for check_row in range(row - 1, row + 2):
        row_numbers = get_row_numbers(map, check_row, col - 1)
        if row_numbers:
            numbers += row_numbers

    if len(numbers) == 2:
        return numbers[0] * numbers[1]
    return 0
    
def get_gear_ratios(map):
    gear_ratio_total = 0
    for row in range(1, len(map) - 1):
        for col in range(1, len(map[row]) - 1):
            if map[row][col] == '*':
                gear_ratio_total += get_ratio(map, row, col)
                
    return gear_ratio_total

def pad_map(map):
    new_map = ['.' + line + '.' for line in map]
    return ['.' * len(new_map[0])] + new_map + ['.' * len(new_map[0])] 

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]
    
    padded_map = pad_map(lines)
    print(get_count_parts(padded_map))
    print(get_gear_ratios(padded_map))

if __name__ == '__main__':
    main()
