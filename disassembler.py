import sys

input_filename = input(
    "Enter the filename/path for the hex instruction file: ")
output_filename = input_filename.split(".")[0] + ".s"

input_file = open(input_filename, "r")
output_file = open(output_filename, "w")

hex_instructions = input_file.read()
hex_instructions = hex_instructions.splitlines()
binary_list = []
for hex_code in hex_instructions:
    integer = int(hex_code, 16)
    binary = format(integer, '0>32b')
    binary_list.append(binary)

instruction_list = [""]*len(hex_instructions)
instruction_count = 0
label_count = 1
for binary in binary_list:
    instruction = ""
    opcode = binary[-7:]
    # R-type instruction handler
    if opcode == '0110011':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        rs2 = binary[-25:-20]
        funct7 = binary[-32:-25]

        if funct7 == '0000000':
            if funct3 == '000':
                instruction += "add "
            elif funct3 == '100':
                instruction += "xor "
            elif funct3 == '110':
                instruction += "or "
            elif funct3 == '111':
                instruction += "and "
            elif funct3 == '001':
                instruction += "sll "
            elif funct3 == '101':
                instruction += "srl "
            else:
                print("Unrecognized funct3 field for R-type instruction")
                input_file.close()
                output_file.close()
                exit()

        elif funct7 == '0100000':
            if funct3 == '000':
                instruction += "sub "
            elif funct3 == '101':
                instruction += "sra "
            else:
                print("Unrecognized funct3 field for R-type instruction")
                input_file.close()
                output_file.close()
                exit()
        else:
            print("Unrecognized funct7 field for R-type instruction")
            input_file.close()
            output_file.close()
            exit()
        rd = str(int(rd, 2))
        rs1 = str(int(rs1, 2))
        rs2 = str(int(rs2, 2))
        instruction = instruction + "x" + rd + ", x" + rs1 + ", x" + rs2

    # I-type (non-load) instruction handler
    elif opcode == '0010011':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        immediate = binary[-32:-20]
        if funct3 == '000':
            instruction += "addi "
        elif funct3 == '100':
            instruction += "xori "
        elif funct3 == '110':
            instruction += "ori "
        elif funct3 == '111':
            instruction += "andi "
        elif funct3 == '001':
            instruction += "slli "
        elif funct3 == '101':
            # srli or srai
            if immediate[:6] == '000000':
                instruction += 'srli '
            elif immediate[:6] == '010000':
                instruction += 'srai '
            else:
                print("Unrecognized immediate field for srli/srai instruction")
                input_file.close()
                output_file.close()
                exit()
            immediate = immediate[6:]
        else:
            print("Unrecognized funct3 field for I-type instruction")
            input_file.close()
            output_file.close()
            exit()

        rd = str(int(rd, 2))
        rs1 = str(int(rs1, 2))
        if immediate[0] == '1':
            immediate = str(-2**11 + int(immediate[1:], 2))
        else:
            immediate = str(int(immediate, 2))
        instruction += "x" + rd + ", x" + rs1 + ", " + immediate

    # I-type Load Instruction handler
    elif opcode == '0000011':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        immediate = binary[-32:-20]
        if funct3 == '000':
            instruction += 'lb '
        elif funct3 == '001':
            instruction += 'lh '
        elif funct3 == '010':
            instruction += 'lw '
        elif funct3 == '011':
            instruction += 'ld '
        elif funct3 == '100':
            instruction += 'lbu '
        elif funct3 == '101':
            instruction += 'lhu '
        elif funct3 == '111':
            instruction += 'lwu '
        else:
            print("Unrecognized funct3 field for load instruction opcode")
            input_file.close()
            output_file.close()
            exit()

        rd = str(int(rd, 2))
        rs1 = str(int(rs1, 2))
        if immediate[0] == '1':
            immediate = str(-2**11 + (int(immediate[1:], 2)))
        else:
            immediate = str(int(immediate, 2))

        instruction += 'x' + rd + ', ' + immediate + '(x' + rs1 + ')'
    # S-type Instruction handler

    elif opcode == '0100011':
        immediate = binary[:7] + binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        rs2 = binary[-25:-20]

        if funct3 == '000':
            instruction += 'sb '
        elif funct3 == '001':
            instruction += 'sh '
        elif funct3 == '010':
            instruction += 'sw '
        elif funct3 == '011':
            instruction += 'sd '
        else:
            print("Unrecognized funct3 field for S-type instruction")
            input_file.close()
            output_file.close()
            exit()

        rs1 = str(int(rs1, 2))
        rs2 = str(int(rs2, 2))
        if immediate[0] == '1':
            immediate = str(-2**11 + int(immediate[1:], 2))
        else:
            immediate = str(int(immediate, 2))

        instruction += 'x' + rs2 + ', ' + immediate + '(x' + rs1 + ')'

    # B-type instruction handler
    # Assuming offset is positive
    elif opcode == '1100011':
        immediate = binary[-32] + binary[-8] + binary[-31:-25] + binary[-12:-8]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        rs2 = binary[-25:-20]

        if funct3 == '000':
            instruction += 'beq '
        elif funct3 == '001':
            instruction += 'bne '
        elif funct3 == '100':
            instruction += 'blt '
        elif funct3 == '101':
            instruction += 'bge '
        elif funct3 == '110':
            instruction += 'bltu '
        elif funct3 == '111':
            instruction += 'bgeu '
        else:
            print("Unrecognized funct3 field for B-type instruction")
            input_file.close()
            output_file.close()
            exit()

        immediate = 2 * int(immediate, 2)
        rs1 = str(int(rs1, 2))
        rs2 = str(int(rs2, 2))
        temp_label = label_count
        temp_instruction = instruction_list[instruction_count +
                                            int(immediate/4)]
        if temp_instruction and temp_instruction[0] == 'L':
            label_count = temp_instruction[1]

        instruction += 'x' + rs1 + ', x' + rs2 + ", L" + str((label_count))
        instruction_list[instruction_count +
                         int(immediate / 4)] = "L" + str((label_count)) + ": "
        label_count = temp_label
        label_count += 1

    # jal handler:
    elif opcode == '1101111':
        immediate = binary[-32] + binary[-20:-12] + \
            binary[-21] + binary[-31:-21]
        rd = binary[-12:-7]
        instruction += 'jal '

        immediate = 2 * int(immediate, 2)
        rd = str(int(rd, 2))

        temp_label = label_count
        temp_instruction = instruction_list[instruction_count +
                                            int(immediate/4)]
        if temp_instruction and temp_instruction[0] == 'L':
            label_count = temp_instruction[1]

        instruction += 'x' + rd + ', L' + str((label_count))
        instruction_list[instruction_count +
                         int(immediate/4)] = "L" + str((label_count)) + ": "
        label_count = temp_label
        label_count += 1
    # jalr handler
    elif opcode == '1100111':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        immediate = binary[-32:-20]

        if funct3 == '000':
            instruction += 'jalr '
        else:
            print("Unrecognized funct3 field for jalr instruction")
            input_file.close()
            output_file.close()
            exit()

        rd = str(int(rd, 2))
        rs1 = str(int(rs1, 2))
        immediate = str(int(immediate, 2))

        instruction += 'x' + rd + ', ' + immediate + '(x' + rs1 + ')'

    # lui handler
    elif opcode == '0110111':
        immediate = binary[-32:-12]
        rd = binary[-12:-7]
        rd = str(int(rd, 2))
        instruction += 'lui '
        instruction += 'x' + rd + ', ' + hex(int(immediate, 2))

    else:
        print("Unrecognized OpCode")
        input_file.close()
        output_file.close()
        exit()

    instruction_list[instruction_count] += instruction
    output_file.write(instruction_list[instruction_count])
    output_file.write("\n")
    instruction_count += 1
input_file.close()
output_file.close()
