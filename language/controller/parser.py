class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def parse(self):
        statements = []
        while self.current_index < len(self.tokens):
            token = self.peek()
            
            if token is None:  # Se não houver mais tokens, pare o processo
                break
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def consume(self, token_type):
        if self.peek()[0] == token_type:
            token = self.tokens[self.current_index]
            self.current_index += 1  # Avançar o índice
            return token
        else:
            raise SyntaxError(f"Esperado {token_type}, mas encontrado {self.peek()[0]}")

    def parse_statement(self):
        token = self.peek()        
        if token[0] == "VAR":
            return self.parse_var_declaration()
        elif token[0] == "CONDITION":  # "if" -> "condition"
            return self.parse_condition_statement()
        elif token[0] == "ALTERNATIVE":  # "else" -> "alternative"
            return self.parse_alternative_statement()
        elif token[0] == "OUTPUT":  # "return" -> "output"
            return self.parse_output_statement()

        # Adicionando tratamento para outros identificadores
        self.consume(token[0])
        return None

    def parse_var_declaration(self):
        self.consume("VAR")  # Consome o "VAR"
        var_name = self.consume("IDENTIFIER")[1]  # Consome o identificador
        self.consume("ASSIGN")  # Consome o operador de atribuição
        value = self.consume("NUMBER")[1]  # Consome o número
        self.consume("SEMICOLON")  # Consome o ponto e vírgula
        return {"type": "var_declaration", "name": var_name, "value": value}

    def parse_condition_statement(self):
        self.consume("CONDITION")  # Consome a "condition"
        self.consume("LPAREN")  # Consumir o parêntese esquerdo
        condition = self.parse_condition()  # Condição dentro da condition
        self.consume("RPAREN")  # Consumir o parêntese direito
        self.consume("LBRACE")  # Consumir a chave de abertura do bloco
        body = self.parse_body()  # Bloco de comandos dentro da condition
        self.consume("RBRACE")  # Consumir a chave de fechamento do bloco
        
        # Verificando se existe um bloco 'alternative'
        alternative_statement = None
        if self.peek() and self.peek()[0] == "ALTERNATIVE":
            alternative_statement = self.parse_alternative_statement()
        
        return {"type": "condition_statement", "condition": condition, "body": body, "alternative": alternative_statement}

    def parse_alternative_statement(self):
        self.consume("ALTERNATIVE")  # Consome o "alternative"
        self.consume("LBRACE")  # Consumir a chave de abertura do bloco 'alternative'
        body = self.parse_body()  # Bloco de comandos dentro do 'alternative'
        self.consume("RBRACE")  # Consumir a chave de fechamento do bloco 'alternative'
        return {"type": "alternative_statement", "body": body}

    def parse_condition(self):
        left_operand = self.consume("IDENTIFIER")[1]  # Consome o identificador (x)
        
        operator_token = self.peek()  # Verifica o próximo token
        if operator_token and operator_token[0] == "ASSIGN":
            operator = "="  # O operador de atribuição
            self.consume("ASSIGN")  # Consome o operador '='
        elif operator_token and operator_token[0] == "EQUALS":
            operator = "=="  # O operador de comparação
            self.consume("EQUALS")  # Consome o operador '=='
        else:
            raise SyntaxError(f"Esperado operador de atribuição ou comparação, mas encontrado {operator_token}")

        right_operand = self.consume("NUMBER")[1]  # Consome o número (5)
        
        return {"left_operand": left_operand, "operator": operator, "right_operand": right_operand}

    def parse_body(self):
        body = []
        token = self.peek()
        while token and token[0] != "RBRACE":  # Enquanto não encontrar a chave de fechamento
            print(f"Parsing token in body: {token}")  # Debug
            body.append(self.parse_statement())  # Analisa as instruções dentro do bloco
            token = self.peek()  # Avança para o próximo token
        return body

    def parse_output_statement(self):
        self.consume("OUTPUT")  # Consome o "output"
        next_token = self.peek()
        if next_token[0] == "IDENTIFIER":
            value = self.consume("IDENTIFIER")[1]
        elif next_token[0] == "NUMBER":
            value = self.consume("NUMBER")[1]
        else:
            raise SyntaxError(f"Esperado IDENTIFIER ou NUMBER, mas encontrado {next_token[0]}")
        self.consume("SEMICOLON")  # Consome o ponto e vírgula
        return {"type": "output_statement", "value": value}

    def peek(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        else:
            return None  # Retorna None quando todos os tokens foram consumidos