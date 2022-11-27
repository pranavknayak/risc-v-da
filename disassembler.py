input_file = open("Input.txt", "r")
output_file = open("Output.s", "w")

hex_instructions = input_file.read()
hex_instructions = hex_instructions.splitlines()
for hex in hex_instructions:
    integer = int(hex, 16)
    binary = format(integer, '0>32b')
    output_file.write(binary)
    output_file.write('\n')

input_file.close()
output_file.close()
