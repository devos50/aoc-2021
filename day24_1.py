import random

instructions = []
regs = [0, 0, 0, 9]


def is_num(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


with open("data/day24.txt") as in_file:
    for line in in_file.readlines():
        parts = line.strip().split(" ")
        instructions.append(parts)


def reset():
    global regs
    regs = [0, 0, 0, 0]


def run_program(inputs):
    for parts in instructions:
        input_ind = 0
        instruction = parts[0]
        if instruction == "inp":
            target_reg = ord(parts[1][0]) - ord('w')
            regs[target_reg] = inputs[input_ind]
            input_ind += 1
        else:
            target_reg1 = ord(parts[1][0]) - ord('w')
            operand2 = int(parts[2]) if is_num(parts[2]) else regs[ord(parts[2][0]) - ord('w')]

            if instruction == "add":
                regs[target_reg1] = regs[target_reg1] + operand2
            elif instruction == "mul":
                regs[target_reg1] = regs[target_reg1] * operand2
            elif instruction == "div":
                regs[target_reg1] = regs[target_reg1] // operand2
            elif instruction == "mod":
                regs[target_reg1] = regs[target_reg1] % operand2
            elif instruction == "eql":
                regs[target_reg1] = 1 if regs[target_reg1] == operand2 else 0


while True:
    num = ''.join(random.choice('123456789') for _ in range(3))
    z_in = random.randint(5000, 12000)
    regs[3] = z_in
    run_program([int(n) for n in list(num)])
    if regs[3] == 0:
        print("%s valid! (z in: %d)" % (num, z_in))
    reset()
