class Tape:
    def __init__(self, input_1, input_2):
        self.tape_1 = [' '] + list(input_1) + [' ']
        self.tape_2 = [' '] + list(input_2) + [' ']
        self.result_tape = [' '] * (max(len(input_1), len(input_2))+1)
        self.normalize()
    
    def normalize(self):
        if len(self.tape_2) < len(self.tape_1):
            self.tape_2[1:] = ['0'] * (len(self.tape_1) - len(self.tape_2)) + self.tape_2[1:]
        else:
            self.tape_1[1:] = ['0'] * (len(self.tape_2) - len(self.tape_1)) + self.tape_1[1:]


class TuringMachine:
    def __init__(self, tape_1, tape_2, result_tape):
        self.tape_1 = tape_1
        self.tape_2 = tape_2
        self.result_tape = result_tape
        self.direction = "right"
        self.state = "start"
        self.head_position = 0
        self.sum = 0
        self.carry = 0
    
    def move_head(self, direction):
        if direction == 'left':
            self.head_position -= 1
        else:
            self.head_position += 1

    def set_state(self, symbol_1, symbol_2, state):
        if (symbol_1 == " " and symbol_2 == " ") and state == "start":
            self.state = "add"
            self.direction = "left"
            self.move_head(self.direction)
        
        if (symbol_1 == symbol_2 == " ") and state == "add":
            self.state = "halt"

    def get_tape_value(self, tape, index):
            if 0 <= index < len(tape):
                return tape[index]
            else:
                return " "
    
    def run(self):
        # move head to the end of the longer tape
        while self.state != "halt":
            self.move_head(self.direction)
            symbol_1 = self.get_tape_value(self.tape_1, self.head_position)
            symbol_2 = self.get_tape_value(self.tape_2, self.head_position)
            self.set_state(symbol_1, symbol_2, self.state)

            if self.state == "add":
                symbol_1 = self.get_tape_value(self.tape_1, self.head_position)
                symbol_2 = self.get_tape_value(self.tape_2, self.head_position)
                self.sum = self.carry
                self.sum += int(symbol_1) if symbol_1 == '1' else 0
                self.sum += int(symbol_2) if symbol_2 == '1' else 0
                self.result_tape[self.head_position] = ('1' if self.sum % 2 == 1 else '0')
                self.carry = 0 if self.sum < 2 else 1

        # handle carry after the while loop
        if self.carry != 0:
            self.result_tape[0] = '1'

        return self.result_tape if self.result_tape[0] != 0 else self.result_tape[1:]


bin_1 = "11101010111"
bin_2 = "111010111"
tape = Tape(bin_1, bin_2)
turing_machine = TuringMachine(tape.tape_1, tape.tape_2, tape.result_tape)
print(turing_machine.run())
