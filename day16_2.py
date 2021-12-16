import numpy

packet = None

with open("data/day16.txt") as in_file:
    hex_str = in_file.read()
    packet = bin(int(hex_str, 16))[2:].zfill(len(hex_str * 4))

print("Packet: %s" % packet)


def parse_packet_header(cur_bit):
    global sum_of_versions
    version = int(packet[cur_bit:cur_bit + 3], 2)
    cur_bit += 3
    packet_id = int(packet[cur_bit:cur_bit + 3], 2)
    cur_bit += 3
    return cur_bit, version, packet_id


def parse_literal_packet(cur_bit):
    literal_bin_str = ""
    while True:
        leading_group_digit = packet[cur_bit]
        cur_bit += 1
        literal_bin_str += packet[cur_bit:cur_bit + 4]
        cur_bit += 4

        if leading_group_digit == '0':  # Last group, we're done
            break

    value = int(literal_bin_str, 2)
    print("Found value: %d" % value)
    return cur_bit, value


def parse_operator_packet(cur_bit, packet_id):
    print("Parsing operator packet")
    length_id_type = packet[cur_bit]
    cur_bit += 1
    values = []
    if length_id_type == '0':
        total_subpacket_length = int(packet[cur_bit:cur_bit+15], 2)
        cur_bit += 15
        subpacket_start = cur_bit
        while cur_bit != subpacket_start + total_subpacket_length:
            cur_bit, value = parse_packet(cur_bit)
            values.append(value)
    else:
        num_subpackets = int(packet[cur_bit:cur_bit+11], 2)
        cur_bit += 11
        for _ in range(num_subpackets):
            cur_bit, value = parse_packet(cur_bit)
            values.append(value)

    # Compute value
    if packet_id == 0:
        return cur_bit, numpy.sum(values)
    elif packet_id == 1:
        return cur_bit, numpy.prod(values)
    elif packet_id == 2:
        return cur_bit, numpy.min(values)
    elif packet_id == 3:
        return cur_bit, numpy.max(values)
    elif packet_id == 5:
        return cur_bit, (1 if values[0] > values[1] else 0)
    elif packet_id == 6:
        return cur_bit, (1 if values[0] < values[1] else 0)
    elif packet_id == 7:
        return cur_bit, (1 if values[0] == values[1] else 0)
    else:
        raise RuntimeError("Unsupported operation!")


def parse_packet(cur_bit):
    cur_bit, version, packet_id = parse_packet_header(cur_bit)
    if packet_id == 4:  # Literal value
        cur_bit, value = parse_literal_packet(cur_bit)
    else:  # Operator packet
        cur_bit, value = parse_operator_packet(cur_bit, packet_id)

    return cur_bit, value


cur_bit, value = parse_packet(0)
print(value)
