"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [bin(0)] * 256
        self.reg = [bin(0)] * 8
        self.pc = 0

        self.branchtable = {}
        self.branchtable['ldi'] = self.handle_ldi
        self.branchtable['prn'] = self.handle_prn
        self.branchtable['hlt'] = self.handle_hlt
        self.branchtable['mul'] = self.handle_mul

    def handle_ldi(self, operand_a, operand_b):
        self.reg[int(operand_a, 2)] = operand_b
        self.pc += 3

    def handle_prn(self, operand_a):
        print(int(self.reg[int(operand_a, 2)], 2))
        self.pc += 2

    def handle_hlt(self):
        sys.exit(1)
        print("Halted!")

    def handle_mul(self, operand_a, operand_b):
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
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
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


        running = True

        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == mul:
                self.branchtable['mul'](operand_a, operand_b)

            if ir == ldi:
                self.branchtable['ldi'](operand_a, operand_b)

            if ir == prn:
                self.branchtable['prn'](operand_a)
            
            elif ir == hlt:
                self.branchtable['hlt']()

