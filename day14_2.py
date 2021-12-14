import copy

rules = {}
pairs_freqs = {}
element_freqs = {}

with open("data/day14.txt") as in_file:
    parse_rules = False
    for line in in_file.readlines():
        if not parse_rules:
            if line == "\n":
                parse_rules = True
                continue
            else:
                polymer = [c for c in line.strip()]
                for pos in range(len(polymer) - 1):
                    pair = (polymer[pos], polymer[pos + 1])
                    if pair not in pairs_freqs:
                        pairs_freqs[pair] = 0
                    pairs_freqs[pair] += 1

                for c in polymer:
                    if c not in element_freqs:
                        element_freqs[c] = 0
                    element_freqs[c] += 1
        else:
            parts = line.strip().split(" -> ")
            rules[tuple(c for c in parts[0])] = parts[1]

print("Start: %s" % polymer)
print(pairs_freqs)
for step in range(40):
    new_freqs = copy.deepcopy(pairs_freqs)
    for pair in pairs_freqs:
        if pairs_freqs[pair] > 0 and pair in rules:
            # print("Applying rule %s" % str(pair))
            pair_freq = pairs_freqs[pair]
            # print("Freq of pair: %d" % pair_freq)
            new_freqs[pair] -= pairs_freqs[pair]
            new_char = rules[pair]

            if new_char not in element_freqs:
                element_freqs[new_char] = 0
            element_freqs[new_char] += pair_freq

            np = (pair[0], new_char)
            if np not in new_freqs:
                new_freqs[np] = 0
            new_freqs[np] += pair_freq

            np = (new_char, pair[1])
            if np not in new_freqs:
                new_freqs[np] = 0
            new_freqs[np] += pair_freq

            # print(new_freqs)
            # print("---")

    pairs_freqs = new_freqs

    # print("step done")
    # print(pairs_freqs)

frequencies = sorted(element_freqs.values())
print(frequencies[-1] - frequencies[0])
