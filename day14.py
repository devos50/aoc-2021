polymer = []
rules = {}

with open("data/day14.txt") as in_file:
    parse_rules = False
    for line in in_file.readlines():
        if not parse_rules:
            if line == "\n":
                parse_rules = True
                continue
            else:
                polymer = [c for c in line.strip()]
        else:
            parts = line.strip().split(" -> ")
            rules[tuple(c for c in parts[0])] = parts[1]

print("Start: %s" % polymer)
for step in range(10):
    applicable_rules = []
    for insert_pos in range(len(polymer) - 1):  # Insert pos 0 means insertion between two first characters
        rule_key = (polymer[insert_pos], polymer[insert_pos + 1])
        if rule_key in rules:
            applicable_rules.append((insert_pos, rules[rule_key]))

    # Apply rules
    applied = 0
    for pos, new_char in applicable_rules:
        polymer.insert(pos + 1 + applied, new_char)
        # print("Inserting %s at pos %d" % (new_char, pos + 1))
        # print(polymer)
        applied += 1

    #print("After step %d: %s" % (step + 1, polymer))


# Determine frequencies
freq_map = {}
for c in polymer:
    if c not in freq_map:
        freq_map[c] = 0
    freq_map[c] += 1

frequencies = sorted(freq_map.values())
print(frequencies[-1] - frequencies[0])