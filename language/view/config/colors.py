import curses
import re
# Palavras-chave da linguagem (exemplo: instruções de controle de fluxo e declarações)
KEYWORDS = {
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

# Definindo as cores para cada tipo de token
def initialize_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)       # Keywords, operadores, símbolos especiais (vermelho)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)      # Condition (azul claro)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Números (roxo)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Parênteses e chaves (branco)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # Strings (amarelo)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Pontuação (;, etc.)

# Definindo expressões regulares para identificar os tokens
TOKEN_PATTERNS = {
    "KEYWORD": re.compile(r'\b(?:' + '|'.join(KEYWORDS.keys()) + r')\b'),
    "CONDITION": re.compile(r'\bcondition\b'),
    "VAR": re.compile(r'\bvar\b'),
    "NUMBER": re.compile(r'\b\d+\b'),
    "STRING": re.compile(r'\("\([^"]*\)"\)'),
    "SEMICOLON": re.compile(r';'),
    "OPERATION": re.compile(r'|'.join(re.escape(op) for op in OPERATORS.keys())),
    "SPECIAL_SYMBOL": re.compile(r'|'.join(re.escape(sym) for sym in SPECIAL_SYMBOLS.keys()))
}

# Aplica o esquema de cores na linha de acordo com o tipo de token
def apply_color_scheme(stdscr, y, x, line, width):
    pos = 0
    while pos < len(line):
        match = None
        color_pair = curses.color_pair(0)

        # Verifica cada padrão de token e aplica a cor correspondente
        for token_type, pattern in TOKEN_PATTERNS.items():
            match = pattern.match(line, pos)
            if match:
                token_text = match.group(0)
                if token_type == "KEYWORD":
                    color_pair = curses.color_pair(1)
                elif token_type == "VAR":
                    color_pair = curses.color_pair(2)
                elif token_type == "NUMBER":
                    color_pair = curses.color_pair(3)
                elif token_type == "SPECIAL_SYMBOL" or token_type == "OPERATION":
                    color_pair = curses.color_pair(1)  # Vermelho
                elif token_type == "STRING":
                    color_pair = curses.color_pair(5)
                elif token_type == "SEMICOLON":
                    color_pair = curses.color_pair(6)
                break

        # Exibe o texto com a cor correspondente
        if match:
            for i, char in enumerate(token_text):
                if x + pos + i < width:
                    stdscr.addch(y, x + pos + i, char, color_pair)
            pos += len(token_text)
        else:
            # Exibe o caractere padrão em branco se não corresponder a nenhum padrão
            if x + pos < width:
                stdscr.addch(y, x + pos, line[pos], curses.color_pair(0))
            pos += 1
