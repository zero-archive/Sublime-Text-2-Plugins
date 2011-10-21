import sublime, sublime_plugin, re

class BrainfuckInterpretCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("select_all")

        if not self.view.sel()[0].empty():
            self.code = re.sub(r'([^><\+\-\.,\[\]])', '', self.view.substr(self.view.sel()[0]))
            text = self.bf()
            self.view.replace(edit, self.view.sel()[0], text)
            view.sel().clear()

    def bf(self):
        self.cells = {}
        self.pointer = 0
        self.buffer = []
        self.code_pointer = 0
        self.output = ''

        while self.code_pointer < len(self.code):
            self.interpret(self.code[self.code_pointer])
            self.code_pointer += 1

        return self.output

    def interpret(self, command):
        if not self.cells.has_key(self.pointer):
            self.cells[self.pointer] = 0

        if command == '>':
            self.pointer += 1

        elif command == '<':
            self.pointer -= 1

        elif command == '+':
            if self.cells[self.pointer] < 255:
                self.cells[self.pointer] += 1

        elif command == '-':
            if self.cells[self.pointer] > 0:
                self.cells[self.pointer] -= 1

        elif command == '.':
            if self.cells.has_key(self.pointer):
                self.output += chr(self.cells[self.pointer])

        elif command == ',':
            self.view.window().show_input_panel("Type value:", '', self.read_input, None, None)

        elif command == '[':
            if self.cells[self.pointer] == 0:
                loopsection = 1

                while (loopsection > 0) and (self.code_pointer + 1 < len(self.code)):
                    self.code_pointer += 1
                    if self.code[self.code_pointer] == '[':
                        loopsection += 1
                    elif self.code[self.code_pointer] == ']':
                        loopsection -= 1
            else:
                self.buffer.append(self.code_pointer)

        elif command == ']':
            self.code_pointer = self.buffer.pop() - 1

        return True

    def read_input(self, input):
        input = input.encode('ascii','ignore')
        self.cells[self.pointer] = ord(input[0]) if (len(input) > 0) else 0

