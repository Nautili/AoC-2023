import sys

def get_mapping(seed, range):
    for subrange in range:
        if subrange[1] <= seed and seed < subrange[1] + subrange[2]:
            return subrange[0] + seed - subrange[1] 
    return seed

def get_ranges(mapping):
    return [((list(map(int, range.split())))) for range in mapping.strip().split('\n')[1:]]

def overlaps(r1, r2):
    return r1[0] <= r2[1] and r1[1] >= r2[0]

def interval_intersect(r1, r2):
    if not overlaps(r1, r2):
        return
    return((max(r1[0], r2[0]), min(r1[1], r2[1])))

def interval_subtract(interval, removed):
    if not overlaps(interval, removed):
        return interval
    
    new_intervals = []
    if interval[0] < removed[0]:
        new_intervals.append((interval[0], removed[0] - 1))
    if removed[1] < interval[1]:
        new_intervals.append((removed[1] + 1, interval[1]))
    return new_intervals

def main():
    with open(sys.argv[1]) as f:
        almanac = f.read().split('\n\n')
    
    seeds = [int(seed) for seed in almanac[0].strip().split()[1:]]
    ranges = [get_ranges(mapping) for mapping in almanac[1:]]

    min_seed = sys.maxsize
    for seed in seeds:
        for seed_map in ranges:
            seed = get_mapping(seed, seed_map)
        min_seed = min(min_seed, seed) 
    
    print(min_seed)

    intervals = [((start, start + size - 1)) for start, size in zip(seeds[0::2], seeds[1::2])]
    for seed_map in ranges:
        new_intervals = []
        for row in seed_map:
            for interval in reversed(intervals):
                intersection = interval_intersect(interval, ((row[1], row[1] + row[2] - 1)))
                if intersection:
                    new_intervals.append((intersection[0] - row[1] + row[0], \
                                          intersection[1] - row[1] + row[0]))
                    split_intervals = interval_subtract(interval, intersection)
                    if split_intervals:
                        intervals += (split_intervals)
                    intervals.remove(interval)
        intervals += new_intervals

    print(min(interval[0] for interval in intervals))

if __name__ == '__main__':
    main()
