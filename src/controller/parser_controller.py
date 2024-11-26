class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.variables = {}

    def parse(self):
        while self.position < len(self.tokens):
            token_type, value = self.tokens[self.position]
            if token_type == 'LET':
                self.parse_let()
            elif token_type == 'PRINT':
                self.parse_print()
            elif token_type == 'IF':
                self.parse_if()
            else:
                raise SyntaxError(f"Comando inválido: {value}")

    def parse_let(self):
        self.position += 1
        var_name = self.tokens[self.position][1]
        self.position += 1
        if self.tokens[self.position][1] != '=':
            raise SyntaxError("Erro de sintaxe em declaração de variável")
        self.position += 1
        value = self.evaluate_expression()
        self.variables[var_name] = value

    def parse_print(self):
        self.position += 1
        value = self.evaluate_expression()
        print("Saída:", value)

    def parse_if(self):
        self.position += 1
        condition = self.evaluate_condition()
        if condition:
            self.position += 1
            self.parse()
        else:
            while self.tokens[self.position][0] not in {'ELSE', 'END'}:
                self.position += 1
            if self.tokens[self.position][0] == 'ELSE':
                self.position += 1
                self.parse()
        while self.tokens[self.position][0] != 'END':
            self.position += 1

    def evaluate_expression(self):
        left_value = self.get_term()
        while self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
            operator = self.tokens[self.position][1]
            self.position += 1
            right_value = self.get_term()
            left_value = self.apply_operator(left_value, operator, right_value)
        return left_value

    def get_term(self):
        token_type, value = self.tokens[self.position]
        if token_type == 'NUMBER':
            self.position += 1
            return int(value)
        elif token_type == 'IDENTIFIER':
            self.position += 1
            if value in self.variables:
                return self.variables[value]
            else:
                raise NameError(f"Variável não definida: {value}")
        else:
            raise SyntaxError(f"Expressão inválida: {value}")

    def evaluate_condition(self):
        left = self.evaluate_expression()
        operator = self.tokens[self.position][1]
        self.position += 1
        right = self.evaluate_expression()
        return self.apply_operator(left, operator, right)

    def apply_operator(self, left, operator, right):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '==':
            return left == right
        else:
            raise SyntaxError(f"Operador desconhecido: {operator}")
