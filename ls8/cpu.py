"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = False


# - `PC`: Program Counter, address of the currently executing instruction
# - `IR`: Instruction Register, contains a copy of the currently executing instruction
# - `MAR`: Memory Address Register, holds the memory address we're reading or writing
# - `MDR`: Memory Data Register, holds the value to write or the value just read
# - `FL`: Flags, see below


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # This is the workhorse function of the entire processor. It's the most difficult
        # part to write.

        # It needs to read the memory address that's stored in register `PC`, and store
        # that result in `IR`, the _Instruction Register_. This can just be a local
        # variable in `run()`.
        running = True
        while running:
            IR = self.ram_read(self.pc)
            # Some instructions requires up to the next two bytes of data _after_ the `PC` in
            # memory to perform operations on. Sometimes the byte value is a register number,
            # other times it's a constant value (in the case of `LDI`). Using `ram_read()`,

            # read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
            operand_a = self.ram_read(self.pc + 1)
            # `operand_b` in case the instruction needs them.
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False

            elif IR == LDI:
                """`LDI register immediate`

                Set the value of a register to an integer.

                Machine code:

                ```
                10000010 00000rrr iiiiiiii
                82 0r ii
    ```"""
                self.reg[operand_a] = operand_b

                self.pc += 3

            elif IR == PRN:
                """
                PRN register pseudo-instruction

                Print numeric value stored in the given register.

                Print to the console the decimal integer value that is stored in the given
                register.

                Machine code:

                01000111 00000rrr
                47 0r
                """

                print(self.reg[operand_a])
                self.pc += 2

        # Then, depending on the value of the opcode, perform the actions needed for the
        # instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other
        # options, too.

        # After running code for any particular instruction, the `PC` needs to be updated
        # to point to the next instruction for the next iteration of the loop in `run()`.
        # The number of bytes an instruction uses can be determined from the two high bits
        # (bits 6-7) of the instruction opcode. See the LS-8 spec for details.

    def ram_read(self, MAR):
        """ should accept the address to read and return the value stored there. """
        # The MAR contains the address that is being read or written to
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """  should accept a value to write, and the address to write it to. """
        # The MDR contains the data that was read or the data to write.

        self.ram[MAR] = MDR
