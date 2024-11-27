class Parser:
    """
    A simple parser for a custom scripting language that supports variable assignments, 
    conditional statements, and expressions. 

    Attributes:
        tokens (list): A list of tokens, each represented as a tuple (type, value).
        position (int): Current position in the token list.
        variables (dict): A dictionary to store variable names and their values.
    """
    def __init__(self, tokens):
        """
        Initialize the parser with a list of tokens and set initial state.

        Args:
            tokens (list): The list of tokens to be parsed.
        """
        self.tokens = tokens
        self.position = 0
        self.variables = {}

    def parse(self):
        """
        Parse the list of tokens and execute commands accordingly.
        Supports commands: LET, PRINT, and IF.
        """
        while self.position < len(self.tokens):
            token_type, value = self.tokens[self.position]
            if token_type == 'LET':
                self.parse_let()
            elif token_type == 'PRINT':
                self.parse_print()
            elif token_type == 'IF':
                self.parse_if()
            else:
                raise SyntaxError(f"Invalid command: {value}")

    def parse_let(self):
        """
        Parse a variable assignment command (LET).
        Syntax: LET <variable_name> = <expression>
        """
        self.position += 1
        var_name = self.tokens[self.position][1]  # Get the variable name
        self.position += 1
        if self.tokens[self.position][1] != '=':
            raise SyntaxError("Syntax error in variable declaration")
        self.position += 1
        value = self.evaluate_expression()  # Evaluate the right-hand expression
        self.variables[var_name] = value  # Store the variable in the dictionary

    def parse_print(self):
        """
        Parse and execute a PRINT command.
        Syntax: PRINT <expression>
        """
        self.position += 1
        value = self.evaluate_expression()  # Evaluate the expression to print
        print("Output:", value)

    def parse_if(self):
        """
        Parse and execute an IF conditional command.
        Syntax: IF <condition> THEN <commands> [ELSE <commands>] END
        """
        self.position += 1
        condition = self.evaluate_condition()  # Evaluate the conditional expression
        if condition:
            self.position += 1
            self.parse()  # Execute commands inside the IF block
        else:
            # Skip tokens until ELSE or END is encountered
            while self.tokens[self.position][0] not in {'ELSE', 'END'}:
                self.position += 1
            if self.tokens[self.position][0] == 'ELSE':
                self.position += 1
                self.parse()  # Execute commands inside the ELSE block
        # Skip remaining tokens in the IF-ELSE block until END is found
        while self.tokens[self.position][0] != 'END':
            self.position += 1

    def evaluate_expression(self):
        """
        Evaluate a mathematical or logical expression.
        Supports operators: +, -, *, /, >, <, ==.

        Returns:
            The evaluated result of the expression.
        """
        left_value = self.get_term()  # Get the first term of the expression
        while self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
            operator = self.tokens[self.position][1]  # Get the operator
            self.position += 1
            right_value = self.get_term()  # Get the next term
            left_value = self.apply_operator(left_value, operator, right_value)
        return left_value

    def get_term(self):
        """
        Get a single term in an expression. A term can be a number or a variable.

        Returns:
            int: The value of the term.

        Raises:
            NameError: If an undefined variable is referenced.
            SyntaxError: If the term is invalid.
        """
        token_type, value = self.tokens[self.position]
        if token_type == 'NUMBER':
            self.position += 1
            return int(value)
        elif token_type == 'IDENTIFIER':
            self.position += 1
            if value in self.variables:
                return self.variables[value]
            else:
                raise NameError(f"Undefined variable: {value}")
        else:
            raise SyntaxError(f"Invalid expression: {value}")

    def evaluate_condition(self):
        """
        Evaluate a conditional expression.
        Supports relational operators: >, <, ==.

        Returns:
            bool: The result of the condition.
        """
        left = self.evaluate_expression()  # Evaluate the left-hand side expression
        operator = self.tokens[self.position][1]  # Get the comparison operator
        self.position += 1
        right = self.evaluate_expression()  # Evaluate the right-hand side expression
        return self.apply_operator(left, operator, right)

    def apply_operator(self, left, operator, right):
        """
        Apply a mathematical or logical operator to two operands.

        Args:
            left: The left operand.
            operator (str): The operator to apply.
            right: The right operand.

        Returns:
            The result of the operation.

        Raises:
            SyntaxError: If an unknown operator is encountered.
        """
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
            raise SyntaxError(f"Unknown operator: {operator}")
