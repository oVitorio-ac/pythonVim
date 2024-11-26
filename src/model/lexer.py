import re

TOKENS = {
    'LET': r'\blet\b',
    'PRINT': r'\bprint\b',
    'IF': r'\bif\b',
    'ELSE': r'\belse\b',
    'END': r'\bend\b',
    'NUMBER': r'\b\d+\b',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'OPERATOR': r'[+\-*/]',
    'COMPARISON': r'[><=]+'
}

def lexer(code):
    tokens = []
    code = code.strip()
    while code:
        match = None
        for token_type, pattern in TOKENS.items():
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                tokens.append((token_type, match.group(0)))
                code = code[match.end():].strip()
                break
        if not match:
            raise SyntaxError(f"Token desconhecido: {code[:10]}")
    return tokens
