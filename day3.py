binnums_for_oxygen = []
binnums_for_scrubber = []
most_common_bit_for_pos = [[], []]

num_len = 0


def filter_list(for_oxygen, bit_pos_to_consider):
    print("Considering bit index %d" % bit_pos_to_consider)
    global binnums_for_oxygen, binnums_for_scrubber
    freq_zeros = 0
    freq_ones = 0

    lst = binnums_for_oxygen if for_oxygen else binnums_for_scrubber

    for binnum in lst:
        if binnum[bit_pos_to_consider] == '0':
            freq_zeros += 1
        else:
            freq_ones += 1

    # Filter the list
    def oxygen_crit(binnum):
        most_common_bit = '0' if (freq_zeros > freq_ones) else '1'
        keep = (binnum[bit_pos_to_consider] == most_common_bit)
        return keep

    def scrubber_crit(binnum):
        if freq_ones == freq_zeros:
            keep = (binnum[bit_pos_to_consider] == '0')
        else:
            least_common_bit = '0' if (freq_zeros < freq_ones) else '1'
            keep = (binnum[bit_pos_to_consider] == least_common_bit)
        return keep

    return list(filter(oxygen_crit if for_oxygen else scrubber_crit, lst))


with open("data/day3.txt") as in_file:
    for line in in_file.readlines():
        binnum = line.strip()
        binnums_for_oxygen.append(binnum)
        binnums_for_scrubber.append(binnum)
        if not num_len:  # Assuming all input lines have equal length
            print("Setting num length to: %d" % len(binnum))
            num_len = len(binnum)

# Oxygen
for bit_ind in range(num_len):
    binnums_for_oxygen = filter_list(1, bit_ind)
    if len(binnums_for_oxygen) == 1:
        break

# Scrubber
for bit_ind in range(num_len):
    binnums_for_scrubber = filter_list(0, bit_ind)
    if len(binnums_for_scrubber) == 1:
        break


print(binnums_for_oxygen)
print(binnums_for_scrubber)

assert len(binnums_for_oxygen) == 1
assert len(binnums_for_scrubber) == 1

print(int(binnums_for_oxygen[0], 2) * int(binnums_for_scrubber[0], 2))