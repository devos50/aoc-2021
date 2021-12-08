import itertools

num_unique = 0
data = []
digits = [
    [1, 1, 1, 0, 1, 1, 1],  # 0
    [0, 0, 1, 0, 0, 1, 0],  # 1
    [1, 0, 1, 1, 1, 0, 1],  # 2
    [1, 0, 1, 1, 0, 1, 1],  # 3
    [0, 1, 1, 1, 0, 1, 0],  # 4
    [1, 1, 0, 1, 0, 1, 1],  # 5
    [1, 1, 0, 1, 1, 1, 1],  # 6
    [1, 0, 1, 0, 0, 1, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 1, 0, 1, 1],  # 9
]

with open("data/day8.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split("|")
        data.append((parts[0].strip().split(" "), parts[1].strip().split(" ")))


def get_digit(toggled):
    try:
        return digits.index(toggled)
    except ValueError:
        return -1


ans = 0


for signals_in, out_vals in data:
    for assignment in list(itertools.permutations([0, 1, 2, 3, 4, 5, 6])):
        digits_seen = [0] * 10
        for signal_in in signals_in:
            toggled = [0] * 7
            for sig_char in signal_in:
                toggled[assignment[ord(sig_char) - ord('a')]] = 1

            digit_ind = get_digit(toggled)
            if digit_ind != -1:
                digits_seen[digit_ind] += 1

            if all([(d == 1) for d in digits_seen]):
                # We got the right assignment - decode the output
                str_val = ""
                for out_val in out_vals:
                    toggled = [0] * 7
                    for out_chr in out_val:
                        toggled[assignment[ord(out_chr) - ord('a')]] = 1

                    digit_ind = get_digit(toggled)
                    str_val += "%d" % digit_ind
                ans += int(str_val)

print(ans)
