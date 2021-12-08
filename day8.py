num_unique = 0
inputs = []
outputs = []

with open("data/day8.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split("|")
        inputs.append(parts[0].strip())
        outputs.append(parts[1].strip())

for output in outputs:
    output_pieces = output.split(" ")
    for piece in output_pieces:
        if len(piece) in [2, 3, 4, 7]:
            num_unique += 1

print(num_unique)