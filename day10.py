scores = []
close_chars = {'{': '}', '[': ']', '(': ')', '<': '>'}
points = {')': 1, ']': 2, '}': 3, '>': 4}

with open("data/day10.txt") as in_file:
    for line in in_file.readlines():
        score = 0
        valid = True
        s = []
        for c in line.strip():
            if c in "[{(<":
                s.append(c)
            elif c == "]" and s[-1] != "[":
                valid = False
                break
            elif c == "}" and s[-1] != "{":
                valid = False
                break
            elif c == ")" and s[-1] != "(":
                valid = False
                break
            elif c == ">" and s[-1] != "<":
                valid = False
                break
            else:
                s.pop()

        if not valid:
            continue

        # Complete
        for open_char in s[::-1]:
            score *= 5
            score += points[close_chars[open_char]]

        scores.append(score)

print(sorted(scores)[len(scores) // 2])