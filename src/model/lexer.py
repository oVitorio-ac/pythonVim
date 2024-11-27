import re

# Define the regular expression patterns for different token types.
TOKENS = {
    'LET': r'\blet\b',  # Matches the keyword "let" for variable assignment.
    'PRINT': r'\bprint\b',  # Matches the keyword "print" for output commands.
    'IF': r'\bif\b',  # Matches the keyword "if" for conditional statements.
    'ELSE': r'\belse\b',  # Matches the keyword "else" for alternative branches.
    'END': r'\bend\b',  # Matches the keyword "end" to terminate a block.
    'NUMBER': r'\b\d+\b',  # Matches numeric literals.
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',  # Matches variable names.
    'OPERATOR': r'[+\-*/]',  # Matches arithmetic operators: +, -, *, /.
    'COMPARISON': r'[><=]+'  # Matches comparison operators: >, <, ==.
}

def lexer(code):
    """
    Tokenizes a given source code string into a list of tokens.

    Args:
        code (str): The source code to be tokenized.

    Returns:
        list: A list of tokens, where each token is a tuple (token_type, token_value).
              - token_type: The type of the token (e.g., 'LET', 'NUMBER').
              - token_value: The actual text value of the token.

    Raises:
        SyntaxError: If an unknown sequence of characters is encountered.

    Example:
        >>> lexer("let x = 10")
        [('LET', 'let'), ('IDENTIFIER', 'x'), ('OPERATOR', '='), ('NUMBER', '10')]
    """
    tokens = []  # List to store the resulting tokens.
    code = code.strip()  # Remove leading and trailing whitespace.
    
    while code:  # Continue until the entire code is processed.
        match = None  # Variable to track if a token is matched.
        for token_type, pattern in TOKENS.items():
            # Compile the regex for the current token type.
            regex = re.compile(pattern)
            match = regex.match(code)  # Attempt to match the pattern at the start of the code.
            
            if match:  # If a match is found:
                # Append the matched token to the tokens list.
                tokens.append((token_type, match.group(0)))
                # Remove the matched portion from the code and strip remaining whitespace.
                code = code[match.end():].strip()
                break  # Exit the loop as a token has been successfully matched.
        
        if not match:  # If no token matches the current code segment:
            # Raise an error with the first 10 characters of the unrecognized segment.
            raise SyntaxError(f"Unknown token: {code[:10]}")
    
    return tokens
