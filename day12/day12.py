import sys

def get_arrangement_count(line, counts, memo):
    if not line:
        return 0 if counts else 1
    if (line, len(counts)) in memo:
        return memo[(line, len(counts))]
    
    ret_counts = 0
    if line[0] in '.?':
        ret_counts += get_arrangement_count(line[1:], counts, memo)
    if line[0] in '#?':
        # Check that we are not in a bad state
        if counts \
           and counts[0] <= len(line) \
           and '.' not in line[:counts[0]] \
           and (counts[0] >= len(line) or line[counts[0]] != '#'):
            ret_counts += get_arrangement_count(line[counts[0] + 1:], counts[1:], memo)
    
    memo[(line, len(counts))] = ret_counts
    return ret_counts

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]
    
    total_counts = 0
    total_expanded_counts = 0
    for line in lines:
        springs, counts = line.split()
        counts = [int(c) for c in counts.split(',')]
        total_counts += get_arrangement_count(springs, counts, {})
        
        expanded_springs = ((springs + '?') * 5)[:-1]
        expanded_counts = counts * 5
        total_expanded_counts += get_arrangement_count(expanded_springs, expanded_counts, {})

    print(total_counts)
    print(total_expanded_counts)


if __name__ == '__main__':
    main()
