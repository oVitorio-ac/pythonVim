# Palavras-chave da linguagem (exemplo: instruções de controle de fluxo e declarações)
KEYWORDS = {
    "var": "VAR",
    "condition": "CONDITION",  # Alterando "if" para "condition"
    "alternative": "ALTERNATIVE",  # Alterando "else" para "alternative"
    "output": "OUTPUT",  # Alterando "return" para "output"
}


# Operadores suportados pela linguagem
OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "=": "ASSIGN",
    "==": "EQUALS",
    "!=": "NOT_EQUALS",
    "<": "LESS_THAN",
    ">": "GREATER_THAN",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
    # Adicione outros operadores conforme necessário
}

# Símbolos especiais (parênteses, chaves, etc.)
SPECIAL_SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
    # Adicione outros símbolos conforme necessário
}

# Definindo os tipos de tokens para números e identificadores
TOKEN_TYPES = {
    "NUMBER": r'\d+',
    "IDENTIFIER": r'[a-zA-Z_][a-zA-Z_0-9]*',
    "WHITESPACE": r'\s+',
}
