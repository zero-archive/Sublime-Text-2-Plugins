import sublime
import sublime_plugin
import re


class BrainfuckInterpretCommand(sublime_plugin.TextCommand):
    """Implementation of interpreter for Brainfuck"""
    def run(self, edit):
        self.view.run_command("select_all")

        if not self.view.sel()[0].empty():
            self.code = re.sub(r'([^><\+\-\.,\[\]])', '', self.view.substr(self.view.sel()[0]))

            if self.code.count('[') != self.code.count(']'):
                sublime.error_message("BrainfuckInterpret: Bad loops count")
            elif self.code.count(','):
                self.edit = edit
                self.view.window().show_input_panel("BrainfuckInterpret type value:", '', self.read_input, None, None)
            else:
                self.view.replace(edit, self.view.sel()[0], self.bf())
                self.view.sel().clear()

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
        if not self.pointer in self.cells:
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
            if self.pointer in self.cells:
                self.output += chr(self.cells[self.pointer])

        elif command == ',':
            if self.input != []:
                self.cells[self.pointer] = ord(self.input.pop(0))

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
        self.input = list(input.encode('ascii', 'ignore'))
        self.view.replace(self.edit, self.view.sel()[0], self.bf())
        self.view.sel().clear()
