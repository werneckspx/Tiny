#LEXICALANALYSIS

class TokenType:
    # Specials
    TT_UNEXPECTED_EOF = -2
    TT_INVALID_TOKEN = -1
    TT_END_OF_FILE = 0

    # Symbols
    TT_SEMICOLON = 1  # ;
    TT_ASSIGN = 2  # =

    # Logic operators
    TT_EQUAL = 3  # ==
    TT_NOT_EQUAL = 4  # !=
    TT_LOWER = 5  # <
    TT_LOWER_EQUAL = 6  # <=
    TT_GREATER = 7  # >
    TT_GREATER_EQUAL = 8  # >=

    # Arithmetic operators
    TT_ADD = 9  # +
    TT_SUB = 10  # -
    TT_MUL = 11  # *
    TT_DIV = 12  # /
    TT_MOD = 13  # %

    # Keywords
    TT_PROGRAM = 14  # program
    TT_WHILE = 15  # while
    TT_DO = 16  # do
    TT_DONE = 17  # done
    TT_IF = 18  # if
    TT_THEN = 19  # then
    TT_ELSE = 20  # else
    TT_OUTPUT = 21  # output
    TT_TRUE = 22  # true
    TT_FALSE = 23  # false
    TT_READ = 24  # read
    TT_NOT = 25  # not

    # Others
    TT_NUMBER = 26  # number
    TT_VAR = 27  # variable


def tt2str(token_type):
    token_names = {
        # Specials
        TokenType.TT_UNEXPECTED_EOF: "UNEXPECTED_EOF",
        TokenType.TT_INVALID_TOKEN: "INVALID_TOKEN",
        TokenType.TT_END_OF_FILE: "END_OF_FILE",

        # Symbols
        TokenType.TT_SEMICOLON: "SEMICOLON",
        TokenType.TT_ASSIGN: "ASSIGN",

        # Logic operators
        TokenType.TT_EQUAL: "EQUAL",
        TokenType.TT_NOT_EQUAL: "NOT_EQUAL",
        TokenType.TT_LOWER: "LOWER",
        TokenType.TT_LOWER_EQUAL: "LOWER_EQUAL",
        TokenType.TT_GREATER: "GREATER",
        TokenType.TT_GREATER_EQUAL: "GREATER_EQUAL",

        # Arithmetic operators
        TokenType.TT_ADD: "ADD",
        TokenType.TT_SUB: "SUB",
        TokenType.TT_MUL: "MUL",
        TokenType.TT_DIV: "DIV",
        TokenType.TT_MOD: "MOD",

        # Keywords
        TokenType.TT_PROGRAM: "PROGRAM",
        TokenType.TT_WHILE: "WHILE",
        TokenType.TT_DO: "DO",
        TokenType.TT_DONE: "DONE",
        TokenType.TT_IF: "IF",
        TokenType.TT_THEN: "THEN",
        TokenType.TT_ELSE: "ELSE",
        TokenType.TT_OUTPUT: "OUTPUT",
        TokenType.TT_TRUE: "TRUE",
        TokenType.TT_FALSE: "FALSE",
        TokenType.TT_READ: "READ",
        TokenType.TT_NOT: "NOT",

        # Others
        TokenType.TT_NUMBER: "NUMBER",
        TokenType.TT_VAR: "VAR",
    }

    if token_type in token_names:
        return token_names[token_type]
    else:
        raise ValueError("Tipo de token inválido")


class Lexeme:
    def __init__(self, token="", type=TokenType.TT_END_OF_FILE):
        self.token = token
        self.type = type

    def __str__(self):
        return f'("{self.token}", {tt2str(self.type)})'


class SymbolTable:
    def __init__(self):
        self.m_symbols = {
            # Symbols
            ";": TokenType.TT_SEMICOLON,
            "=": TokenType.TT_ASSIGN,
            # Logic operators
            "==": TokenType.TT_EQUAL,
            "!=": TokenType.TT_NOT_EQUAL,
            "<": TokenType.TT_LOWER,
            "<=": TokenType.TT_LOWER_EQUAL,
            ">": TokenType.TT_GREATER,
            ">=": TokenType.TT_GREATER_EQUAL,
            # Arithmetic operators
            "+": TokenType.TT_ADD,
            "-": TokenType.TT_SUB,
            "*": TokenType.TT_MUL,
            "/": TokenType.TT_DIV,
            "%": TokenType.TT_MOD,
            # Keywords
            "program": TokenType.TT_PROGRAM,
            "while": TokenType.TT_WHILE,
            "do": TokenType.TT_DO,
            "done": TokenType.TT_DONE,
            "if": TokenType.TT_IF,
            "then": TokenType.TT_THEN,
            "else": TokenType.TT_ELSE,
            "output": TokenType.TT_OUTPUT,
            "true": TokenType.TT_TRUE,
            "false": TokenType.TT_FALSE,
            "read": TokenType.TT_READ,
            "not": TokenType.TT_NOT,
        }

    def contains(self, token):
        return token in self.m_symbols

    def find(self, token):
        return self.m_symbols.get(token, TokenType.TT_VAR)


class LexicalAnalysis:
    def __init__(self, filename):
        self.m_line = 1
        self.m_st = SymbolTable()
        self.m_input = open(filename, "r")
        if not self.m_input:
            raise Exception("Não foi possível abrir o arquivo")

    def __del__(self):
        if self.m_input:
            self.m_input.close()

    def nextToken(self):
        state = 1
        lex = Lexeme()

        while state != 7 and state != 8:
            c = self.m_input.read(1)

            if state == 1:
                if c in [' ', '\t', '\r']:
                    state = 1
                elif c == '\n':
                    self.m_line += 1
                    state = 1
                elif c == '#':
                    state = 2
                elif c in ['=', '<', '>']:
                    lex.token += c
                    state = 3
                elif c == '!':
                    lex.token += c
                    state = 4
                elif c in [';', '+', '-', '*', '/', '%']:
                    lex.token += c
                    state = 7
                elif c == '_' or c.isalpha():
                    lex.token += c
                    state = 5
                elif c.isdigit():
                    lex.token += c
                    state = 6
                else:
                    if not c:
                        lex.type = TokenType.TT_END_OF_FILE
                        state = 8
                    else:
                        lex.token += c
                        lex.type = TokenType.TT_INVALID_TOKEN
                        state = 8

            elif state == 2:
                if c == '\n':
                    self.m_line += 1
                    state = 1
                elif not c:
                    lex.type = TokenType.TT_END_OF_FILE
                    state = 8
                else:
                    state = 2

            elif state == 3:
                if c == '=':
                    lex.token += c
                    state = 7
                else:
                    if c:
                        self.m_input.seek(self.m_input.tell() - 1)
                    state = 7

            elif state == 4:
                if c == '=':
                    lex.token += c
                    state = 7
                else:
                    if not c:
                        lex.type = TokenType.TT_UNEXPECTED_EOF
                        state = 8
                    else:
                        lex.type = TokenType.TT_INVALID_TOKEN
                        state = 8

            elif state == 5:
                if c == '_' or c.isalpha() or c.isdigit():
                    lex.token += c
                    state = 5
                else:
                    if c:
                        self.m_input.seek(self.m_input.tell() - 1)
                    state = 7

            elif state == 6:
                if c.isdigit():
                    lex.token += c
                    state = 6
                else:
                    if c:
                        self.m_input.seek(self.m_input.tell() - 1)
                    lex.type = TokenType.TT_NUMBER
                    state = 8

        if state == 7:
            lex.type = self.m_st.find(lex.token)

        return lex

'''if __name__ == "__main__":
    lexer = LexicalAnalysis("somatorio.tiny")
    lexeme = lexer.nextToken()

    while lexeme.type != TokenType.TT_END_OF_FILE:
        print(lexeme)
        lexeme = lexer.nextToken()

    lexer.__del__()'''

#INTERPRETER

#MEMORY

class Memory:
    m_memory = {}  # Dicionário para armazenar variáveis e valores inteiros

    @staticmethod
    def read(name):
        return Memory.m_memory.get(name, 0)  # Retorna 0 se a variável não existir

    @staticmethod
    def write(name, value):
        Memory.m_memory[name] = value

#COMAND

class Command:
    def __init__(self, line):
        self.line = line

    def execute(self):
        pass


class AssignCommand(Command):
    def __init__(self, line, variable, expression):
        super().__init__(line)
        self.variable = variable
        self.expression = expression

    def execute(self):
        value = self.expression.expr()
        self.variable.setValue(value)


class BlocksCommand(Command):
    def __init__(self, line):
        super().__init__(line)
        self.commands = []

    def addCommand(self, command):
        self.commands.append(command)

    def execute(self):
        for cmd in self.commands:
            cmd.execute()


class IfCommand(Command):
    def __init__(self, line, condition, then_commands, else_commands=None):
        super().__init__(line)
        self.condition = condition
        self.then_commands = then_commands
        self.else_commands = else_commands

    def execute(self):
        if self.condition.expr():
            self.then_commands.execute()
        elif self.else_commands:
            self.else_commands.execute()


class OutputCommand(Command):
    def __init__(self, line, expression):
        super().__init__(line)
        self.expression = expression

    def execute(self):
        value = self.expression.expr()
        print(value)


class WhileCommand(Command):
    def __init__(self, line, condition, commands):
        super().__init__(line)
        self.condition = condition
        self.commands = commands

    def execute(self):
        while self.condition.expr():
            self.commands.execute()

#BOOL_EXPR
class BoolExpr:
    def __init__(self, line):
        self.line = line

    def expr(self):
        pass

class SingleBoolExpr:
    class Op:
        EQUAL = 0
        NOT_EQUAL = 1
        LOWER = 2
        GREATER = 3
        LOWER_EQUAL = 4
        GREATER_EQUAL = 5

    def __init__(self, line, left, op, right):
        self.line = line
        self.left = left
        self.op = op
        self.right = right

    def expr(self):
        v1 = self.left.expr()
        v2 = self.right.expr()

        if self.op == SingleBoolExpr.Op.EQUAL:
            return v1 == v2
        elif self.op == SingleBoolExpr.Op.NOT_EQUAL:
            return v1 != v2
        elif self.op == SingleBoolExpr.Op.LOWER:
            return v1 < v2
        elif self.op == SingleBoolExpr.Op.LOWER_EQUAL:
            return v1 <= v2
        elif self.op == SingleBoolExpr.Op.GREATER:
            return v1 > v2
        else:  # Assume que é (Maior ou Igual)
            return v1 >= v2

class NotBoolExpr(BoolExpr):
    def __init__(self, line, expr):
        super().__init__(line)
        self.expr = expr

    def expr(self):
        return not self.expr.expr()

class ConstBoolExpr(BoolExpr):
    def __init__(self, line, value):
        self.line = line
        self.value = value

#INT_EXPR
class IntExpr:
    def __init__(self, line):
        self.line = line

    def expr(self):
        pass
            
class BinaryIntExpr:
    class Op:
        ADD = 0
        SUB = 1
        MUL = 2
        DIV = 3
        MOD = 4

    def __init__(self, line, left, op, right):
        self.line = line
        self.left = left
        self.op = op
        self.right = right

    def expr(self):
        v1 = self.left.expr()
        v2 = self.right.expr()

        if self.op == BinaryIntExpr.Op.ADD:
            return v1 + v2
        elif self.op == BinaryIntExpr.Op.SUB:
            return v1 - v2
        elif self.op == BinaryIntExpr.Op.MUL:
            return v1 * v2
        elif self.op == BinaryIntExpr.Op.DIV:
            return int(v1 / v2)
        else:  # Assume que é MOD 
            return v1 % v2

class ConstIntExpr(IntExpr):
    def __init__(self, line, value):
        super().__init__(line)
        self.value = value

    def expr(self):
        return self.value

class Variable(IntExpr):
    def __init__(self, line, name):
        super().__init__(line)
        self.name = name

    def value(self):
        return Memory.read(self.name)

    def setValue(self, value):
        Memory.write(self.name, value)

    def expr(self):
        return self.value()


class NegIntExpr(IntExpr):
    def __init__(self, line, expr):
        super().__init__(line)
        self.expr = expr

    def expr(self):
        return -self.expr.expr()

class ReadIntExpr(IntExpr):
    def __init__(self, line):
        super().__init__(line)

    def expr(self):
        value = int(input())
        return value

#SYNTATIC
class SyntaticAnalysis:
    def __init__(self, lex):
        self.m_lex = lex
        self.m_current = lex.nextToken()

    def start(self):
        cmd = self.procProgram()
        self.eat(TokenType.TT_END_OF_FILE)
        return cmd

    def advance(self):
        self.m_current = self.m_lex.nextToken()

    def eat(self, token_type):
        if token_type == self.m_current.type:
            self.advance()
        else:
            self.showError()

    def showError(self):
        print(f"{str(self.m_lex.m_line).zfill(2)}: ", end='')

        if self.m_current.type == TokenType.TT_INVALID_TOKEN:
            print(f"Lexema inválido [{self.m_current.token}]")
        elif self.m_current.type in [TokenType.TT_UNEXPECTED_EOF, TokenType.TT_END_OF_FILE]:
            print("Fim de arquivo inesperado")
        else:
            print(f"Lexema não esperado [{self.m_current.token}]")

        exit(1)
    # <program>   ::= program <cmdlist>
    def procProgram(self):
        self.eat(TokenType.TT_PROGRAM)
        cmd = self.procCmdList()
        return cmd

    # <cmdlist>   ::= <cmd> { <cmd> }
    def procCmdList(self):
        line = self.m_lex.m_line
        cmds = BlocksCommand(line)

        cmd = self.procCmd()
        cmds.addCommand(cmd)

        while self.m_current.type in [TokenType.TT_VAR, TokenType.TT_OUTPUT, TokenType.TT_IF, TokenType.TT_WHILE]:
            cmd = self.procCmd()
            cmds.addCommand(cmd)

        return cmds

    # <cmd>       ::= (<assign> | <output> | <if> | <while>) ;
    def procCmd(self):
        cmd = None
        if self.m_current.type == TokenType.TT_VAR:
            cmd = self.procAssign()
        elif self.m_current.type == TokenType.TT_OUTPUT:
            cmd = self.procOutput()
        elif self.m_current.type == TokenType.TT_IF:
            cmd = self.procIf()
        elif self.m_current.type == TokenType.TT_WHILE:
            cmd = self.procWhile()
        else:
            self.showError()

        self.eat(TokenType.TT_SEMICOLON)
        return cmd

    # <assign>    ::= <var> = <intexpr>
    def procAssign(self):
        line = self.m_lex.m_line

        var = self.procVar()
        self.eat(TokenType.TT_ASSIGN)
        expr = self.procIntExpr()

        cmd = AssignCommand(line, var, expr)
        return cmd

    # <output>    ::= output <intexpr>
    def procOutput(self):
        self.eat(TokenType.TT_OUTPUT)
        line = self.m_lex.m_line

        if self.m_current.type == TokenType.TT_SUB:
            self.advance()
            if self.m_current.type == TokenType.TT_READ:
                self.advance()
                read_expr = ReadIntExpr(line)
                value = -read_expr.expr()  # Negativa o valor lido
                cmd = OutputCommand(line, ConstIntExpr(line, value))
            else:
                self.showError()
        else:
            expr = self.procIntExpr()
            cmd = OutputCommand(line, expr)

        return cmd

    # <if>        ::= if <boolexpr> then <cmdlist> [ else <cmdlist> ] done
    def procIf(self):
        self.eat(TokenType.TT_IF)
        line = self.m_lex.m_line

        cond = self.procBoolExpr()
        self.eat(TokenType.TT_THEN)
        thenCmds = self.procCmdList()
        elseCmds = None
        if self.m_current.type == TokenType.TT_ELSE:
            self.advance()
            elseCmds = self.procCmdList()
        self.eat(TokenType.TT_DONE)

        cmd = IfCommand(line, cond, thenCmds, elseCmds)
        return cmd

    # <while>     ::= while <boolexpr> do <cmdlist> done
    def procWhile(self):
        self.eat(TokenType.TT_WHILE)
        line = self.m_lex.m_line

        expr = self.procBoolExpr()
        self.eat(TokenType.TT_DO)
        cmds = self.procCmdList()
        self.eat(TokenType.TT_DONE)

        cmd = WhileCommand(line, expr, cmds)
        return cmd


    # <boolexpr>  ::= false | true |
    #                 not <boolexpr> |
    #                 <intterm> (== | != | < | > | <= | >=) <intterm>
    def procBoolExpr(self):
        if self.m_current.type == TokenType.TT_FALSE:
            self.advance()
            return ConstBoolExpr(self.m_lex.m_line, False)
        elif self.m_current.type == TokenType.TT_TRUE:
            self.advance()
            return ConstBoolExpr(self.m_lex.m_line, True)
        elif self.m_current.type == TokenType.TT_NOT:
            self.advance()
            line = self.m_lex.m_line
            expr = self.procBoolExpr()
            return NotBoolExpr(line, expr)
        else:
            line = self.m_lex.m_line
            left = self.procIntTerm()

            op = SingleBoolExpr.Op.EQUAL
            if self.m_current.type == TokenType.TT_EQUAL:
                op = SingleBoolExpr.Op.EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_NOT_EQUAL:
                op = SingleBoolExpr.Op.NOT_EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_LOWER:
                op = SingleBoolExpr.Op.LOWER
                self.advance()
            elif self.m_current.type == TokenType.TT_GREATER:
                op = SingleBoolExpr.Op.GREATER
                self.advance()
            elif self.m_current.type == TokenType.TT_LOWER_EQUAL:
                op = SingleBoolExpr.Op.LOWER_EQUAL
                self.advance()
            elif self.m_current.type == TokenType.TT_GREATER_EQUAL:
                op = SingleBoolExpr.Op.GREATER_EQUAL
                self.advance()
            else:
                self.showError()

            right = self.procIntTerm()

            expr = SingleBoolExpr(line, left, op, right)
            return expr

    # <intexpr>   ::= [ + | - ] <intterm> [ (+ | - | * | / | %) <intterm> ]
    def procIntExpr(self):
        is_negative = False
        if self.m_current.type == TokenType.TT_ADD:
            self.advance()
        elif self.m_current.type == TokenType.TT_SUB:
            self.advance()
            is_negative = True

        if is_negative:
            line = self.m_lex.m_line
            tmp = self.procIntTerm()
            left = NegIntExpr(line, tmp)
        else:
            left = self.procIntTerm()

        if self.m_current.type in [TokenType.TT_ADD, TokenType.TT_SUB, TokenType.TT_MUL, TokenType.TT_DIV, TokenType.TT_MOD]:
            line = self.m_lex.m_line

            op = BinaryIntExpr.Op.ADD
            if self.m_current.type == TokenType.TT_ADD:
                op = BinaryIntExpr.Op.ADD
                self.advance()
            elif self.m_current.type == TokenType.TT_SUB:
                op = BinaryIntExpr.Op.SUB
                self.advance()
            elif self.m_current.type == TokenType.TT_MUL:
                op = BinaryIntExpr.Op.MUL
                self.advance()
            elif self.m_current.type == TokenType.TT_DIV:
                op = BinaryIntExpr.Op.DIV
                self.advance()
            elif self.m_current.type == TokenType.TT_MOD:
                op = BinaryIntExpr.Op.MOD
                self.advance()

            right = self.procIntTerm()

            left = BinaryIntExpr(line, left, op, right)

        return left

    # <intterm>   ::= <var> | <const> | read
    def procIntTerm(self):
        if self.m_current.type == TokenType.TT_VAR:
            return self.procVar()
        elif self.m_current.type == TokenType.TT_NUMBER:
            return self.procConst()
        else:
            self.eat(TokenType.TT_READ)
            line = self.m_lex.m_line
            expr = ReadIntExpr(line)
            return expr

    # <var>       ::= id
    def procVar(self):
        tmp = self.m_current.token

        self.eat(TokenType.TT_VAR)
        line = self.m_lex.m_line

        var = Variable(line, tmp)
        return var

    # <const>     ::= number
    def procConst(self):
        tmp = self.m_current.token

        self.eat(TokenType.TT_NUMBER)
        line = self.m_lex.m_line

        value = int(tmp)
        expr = ConstIntExpr(line, value)
        return expr
    
if __name__ == "__main__":

    lexer = LexicalAnalysis("somatorio.tiny")
    syntactic_analyzer = SyntaticAnalysis(lexer)

    try:
        program = syntactic_analyzer.start()
        if program is not None:
            # Se a análise sintática executa o programa
            program.execute()
    except Exception as e:
        print("Erro ao analisar o programa:", str(e))


