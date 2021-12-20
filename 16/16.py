#!/usr/bin/env python3

import sys


def calculate(calc_type, numbers):
    if calc_type in [5, 6, 7] and len(numbers) < 2:
        print("CANNOT CALCULATE")
        return
    if calc_type == 0:
        value = sum(numbers)
    elif calc_type == 1:
        if len(numbers) == 1:
            value = sum(numbers)
        else:
            value = 1
            for y in numbers:
                value *= y
    elif calc_type == 2:
        value = min(numbers)
    elif calc_type == 3:
        value = max(numbers)
    elif calc_type == 5:
        value = 1 if numbers[0] > numbers[1] else 0
    elif calc_type == 6:
        value = 1 if numbers[0] < numbers[1] else 0
    elif calc_type == 7:
        value = 1 if numbers[0] == numbers[1] else 0
    elif calc_type == 4:
        return
    else:
        raise ValueError(f"calc_type: '{calc_type}'")

    # print("CALC:", numbers, " op:", calc_type, "=", value)
    return value


class Packet:
    def __init__(self, vers, type_p, packets=[]):
        self.vers = vers
        self.type_p = type_p
        self.packets = packets


def transform_data(data):
    bdata = [f"{int(x,16):0>4b}" for x in data]
    return "".join(bdata)


bstr = None
if len(sys.argv) > 1:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = f.readlines()[0].strip()
    bstr = transform_data(data)


def magic(packet, offset=0):
    version = int(packet[offset : offset + 3], 2)
    offset += 3
    versions.append(version)
    type_p = int(packet[offset : offset + 3], 2)
    offset += 3
    # print(f"o={offset-6}, Version: '{version}', type: '{type_p}', packet: '{packet}'")
    print(f"o={offset-6}, Version: '{version}', type: '{type_p}'")

    if type_p == 4:
        # literal
        literal = ""
        while int(packet[offset], 2) != 0:
            literal += packet[offset + 1 : offset + 5]
            offset += 5
        literal += packet[offset + 1 : offset + 5]
        offset += 5

        while len(literal) % 4:
            literal += "0"

        v = int(literal, 2)
        print(" - literal:", v)
        return offset, v
    else:
        vals = []
        len_type = packet[offset]
        offset += 1

        if len_type == "0":
            # Type 0, 15 bits that represent the length
            maxbits = int(packet[offset : offset + 15], 2)
            print("Maxbits", maxbits)
            offset += 15
            inner_offset = offset
            while True:
                next_offset, v = magic(packet, inner_offset)
                vals.append(v)
                inner_offset = next_offset
                if next_offset - offset == maxbits:
                    break
            offset = inner_offset
        elif len_type == "1":
            # Type 1, 11 bits that represent the number of packets
            n_packets = int(packet[offset : offset + 11], 2)
            offset += 11
            print("NumPackets", n_packets)
            for _ in range(n_packets):
                offset, v = magic(packet, offset)
                vals.append(v)
        else:
            raise ValueError("Incorrect len_type.")

        return offset, calculate(type_p, vals)


versions = []
if bstr:
    offset, v = magic(bstr)
    print("\nPart 1:", sum(versions))
    print(f"Part 2: {v}")
else:
    DATA = [
        "8A004A801A8002F478",
        "620080001611562C8802118E34",
        "C0015000016115A2E0802F182340",
        "A0016C880162017C3686B18A3D4780",
        "C200B40A82",
    ]
    ANS = [16, 12, 23, 31, 14]
    for data, ans in zip(DATA, ANS):
        print(" ------------------------------------------ ")
        print(data)
        versions = []
        bstr = transform_data(list(data))
        magic(bstr)
        result = sum(versions)
        if result == ans:
            print("\n ++++ OK ++++ \n")
        else:
            print(f"\n ¡FAILED! {result} != {ans} \n")
            assert False
