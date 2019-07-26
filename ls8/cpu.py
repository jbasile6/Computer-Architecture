"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.fl = 0b00000000 # flags
        self.ram = [bin(0)] * 256
        self.reg = [bin(0)] * 8
        self.pc = 0
        #day 2 mvp
        self.branchtable = {}
        self.branchtable['ldi'] = self.handle_ldi
        self.branchtable['prn'] = self.handle_prn
        self.branchtable['hlt'] = self.handle_hlt
        self.branchtable['mul'] = self.handle_mul
        #day 3 mvp
        self.sp = 255 # stack pointer set to end of ram/ prevents overlap
        self.branchtable['pop'] = self.handle_pop
        self.branchtable['push'] = self.handle_push
        #day 4 mvp
        self.branchtable['call'] = self.handle_call
        self.branchtable['ret'] = self.handle_ret
        self.branchtable['add'] = self.handle_add
        #sprint challenge
        self.branchtable['cmp'] = self.handle_cmp
        self.branchtable['jmp'] = self.handle_jmp
        self.branchtable['jeq'] = self.handle_jeq
        self.branchtable['jne'] = self.handle_jne


    def handle_jne(self):
        print('JNE')
        if self.fl != 1:
            self.handle_jmp()
        else:
            self.pc += 2

    def handle_jeq(self):
        print('JEQ')
        if self.fl == 0b00000001:
            self.handle_jmp()
        else:
            self.pc += 2

    def handle_jmp(self):
        print('JMP')
        reg_addr = self.ram_read(self.pc + 1) #operand_a
        reg_val = self.reg[int(reg_addr, 2)]
        self.pc = int(reg_val, 2)

    def handle_cmp(self, operand_a, operand_b):
        print('CMP')
        self.alu('CMP', operand_a, operand_b)
        self.pc += 3


    def handle_call(self, operand_a):
        print('Call')
        next_instruction = self.pc + 2
        self.ram[self.sp] = bin(next_instruction)
        self.sp -= 1
        change_pc = int(operand_a, 2)
        register_val = self.reg[change_pc]
        self.pc = int(register_val, 2)

    def handle_ret(self):
        print('Return')
        self.sp += 1
        ret_position = self.ram[self.sp]
        self.pc = int(ret_position, 2)

    def handle_add(self, operand_a, operand_b):
        print('Add')
        index1 = int(operand_a, 2)
        index2 = int(operand_b, 2)
        add1 = int(self.reg[index1], 2)
        add2 = int(self.reg[index2], 2)
        sumOfNum = add1 + add2
        self.reg[index1] = bin(sumOfNum)
        self.pc += 3



    def handle_pop(self, operand_a):
        print("POP")
        self.sp += 1
        pop_num = self.ram[self.sp]
        index = int(operand_a, 2)
        self.reg[index] = pop_num

        self.pc += 2

    def handle_push(self, operand_a):
        print('PUSH')
        index = int(operand_a, 2)
        push_num = self.reg[index]
        self.ram[self.sp] = push_num
        self.pc += 2
        self.sp -= 1

    def handle_ldi(self, operand_a, operand_b):
        print('LDI')
        self.reg[int(operand_a, 2)] = operand_b
        self.pc += 3

    def handle_prn(self, operand_a):
        print('PRN')
        print(int(self.reg[int(operand_a, 2)], 2))
        self.pc += 2

    def handle_hlt(self):
        print("Halted")
        sys.exit(1)
        

    def handle_mul(self, operand_a, operand_b):
        print('MUL')
        num1 = self.reg[int(operand_a, 2)]
        num2 = self.reg[int(operand_b, 2)]
        mul_answer =  int(num1, 2) * int(num2, 2)

        self.reg[int(operand_a, 2)] = bin(mul_answer)
        self.pc += 3


    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""

        address = 0
    # commenting out hardcoded program
        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = bin(instruction)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]


        elif op == "CMP": 
            val = int(self.reg[int(reg_a, 2)], 2) - int(self.reg[int(reg_b, 2)], 2)
            # print(val)

            if val == 0: #they are equal
                self.fl = 0b00000001
            elif val > 0: # reg_a is greater
                self.fl = 0b00000010
            else: #reg_b is greater
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #LDI- load immediate
        # store val in a register
        # takes next val in program to find what reg to place it in
        # sets next val to be val of register
        ldi = bin(0b10000010)
        #PRN
        #print something
        # next val tells which reg to print
        prn = bin(0b01000111)
        #HLT- halt command
        hlt = bin(0b00000001)
        #MUL - multiply  command
        mul = bin(0b10100010)
        #PUSH - push command
        push = bin(0b01000101)
        #POP - pop command
        pop= bin(0b01000110)

        call = bin(0b01010000)
        ret = bin(0b00010001)
        add = bin(0b10100000)

        CMP = bin(0b10100111)
        jmp = bin(0b01010100)
        jeq = bin(0b01010101)
        jne = bin(0b01010110)



        running = True

        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == CMP:
                self.branchtable['cmp'](operand_a, operand_b)

            elif ir == jmp:
                self.branchtable['jmp']()

            elif ir == jeq:
                self.branchtable['jeq']()

            elif ir == jne:
                self.branchtable['jne']()

            elif ir == mul:
                self.branchtable['mul'](operand_a, operand_b)

            elif ir == ldi:
                self.branchtable['ldi'](operand_a, operand_b)

            elif ir == prn:
                self.branchtable['prn'](operand_a)

            elif ir == push:
                self.branchtable['push'](operand_a)

            elif ir == pop:
                self.branchtable['pop'](operand_a)

            elif ir == call:
                self.branchtable['call'](operand_a)
            
            elif ir == ret:
                self.branchtable['ret']()

            elif ir == add:
                self.branchtable['add'](operand_a, operand_b)
            
            elif ir == hlt:
                self.branchtable['hlt']()

