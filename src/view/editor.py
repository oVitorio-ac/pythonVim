import curses
import re
from src.model.lexer import lexer
from src.controller.parser_controller import Parser

command_instructions = (
    "Project: Text Editor | Use ESC for Command Mode | "
    "run: Execute the code | edit: Start editing the code | "
    "kill: Terminate the editor | save: Save the file"
)

def display_menu(stdscr, mode, command_text, files, current_file_index):
    height, width = stdscr.getmaxyx()
    
    # Exibir abas com os nomes dos arquivos
    for i, file in enumerate(files):
        tab_text = f"[{file['name']}] "
        color = curses.color_pair(3) if i == current_file_index else curses.color_pair(2)
        stdscr.addstr(height - 1, i * 15, tab_text, color)
    
    # Exibir o texto de comando no modo COMMAND
    if mode == "COMMAND":
        stdscr.addstr(height - 3, 0, ":" + command_text)
    
    # Exibir as instruções de comando
    stdscr.addstr(height - 4, 0, command_instructions)

def handle_viewer_mode(key, cursor_x, cursor_y, scroll_offset, text, command_text):
    mode = "VIEWER"
    if key == 27:  # ESC para entrar no modo de comando
        mode = "COMMAND"
        command_text = ""
    elif key == curses.KEY_UP and cursor_y > 0:
        cursor_y -= 1
        cursor_x = min(cursor_x, len(text[cursor_y]))
    elif key == curses.KEY_DOWN and cursor_y < len(text) - 1:
        cursor_y += 1
        cursor_x = min(cursor_x, len(text[cursor_y]))
    elif key == curses.KEY_LEFT and cursor_x > 0:
        cursor_x -= 1
    elif key == curses.KEY_RIGHT and cursor_x < len(text[cursor_y]):
        cursor_x += 1
    return mode, command_text, cursor_x, cursor_y, scroll_offset

def handle_command_mode(key, command_text, files, current_file_index, stdscr):
    mode = "COMMAND"
    should_exit = False
    if key == 27:  # ESC para sair do modo de comando
        mode = "VIEWER"
        command_text = ""
    elif key == 10:  # Enter
        if command_text == "save":
            save_file(files[current_file_index]["content"], files[current_file_index]["name"])
        elif command_text.startswith("new "):
            filename = command_text.split(" ", 1)[1]
            files.append({"name": filename, "content": [""]})
            current_file_index = len(files) - 1
        elif command_text == "kill":
            should_exit = True
        elif command_text == "edit":
            mode = "EDIT"
        elif command_text == "run":
            # Limpar a tela e mostrar o resultado
            stdscr.clear()
            execute_user_code(files[current_file_index]["content"], stdscr)
            stdscr.addstr("\nPressione qualquer tecla para voltar ao editor...")
            stdscr.refresh()
            stdscr.getch()
            mode = "VIEWER"
        command_text = ""
    elif key == curses.KEY_BACKSPACE or key in [127, 8]:  # Backspace
        command_text = command_text[:-1]
    elif 32 <= key <= 126:
        command_text += chr(key)
    return mode, command_text, should_exit, files, current_file_index

def handle_edit_mode(key, cursor_x, cursor_y, scroll_offset, text):
    mode = "EDIT"
    if key == 27:  # ESC para voltar ao modo VIEWER
        mode = "VIEWER"
    elif key in (curses.KEY_BACKSPACE, 127, 8):
        if cursor_x > 0:
            line = text[cursor_y]
            text[cursor_y] = line[:cursor_x - 1] + line[cursor_x:]
            cursor_x -= 1
        elif cursor_y > 0:
            cursor_x = len(text[cursor_y - 1])
            text[cursor_y - 1] += text.pop(cursor_y)
            cursor_y -= 1
    elif key == curses.KEY_ENTER or key == 10:
        text.insert(cursor_y + 1, text[cursor_y][cursor_x:])
        text[cursor_y] = text[cursor_y][:cursor_x]
        cursor_y += 1
        cursor_x = 0
    elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN):
        if key == curses.KEY_LEFT and cursor_x > 0:
            cursor_x -= 1
        elif key == curses.KEY_RIGHT and cursor_x < len(text[cursor_y]):
            cursor_x += 1
        elif key == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1
            cursor_x = min(cursor_x, len(text[cursor_y]))
        elif key == curses.KEY_DOWN and cursor_y < len(text) - 1:
            cursor_y += 1
            cursor_x = min(cursor_x, len(text[cursor_y]))
    else:
        text[cursor_y] = text[cursor_y][:cursor_x] + chr(key) + text[cursor_y][cursor_x:]
        cursor_x += 1
    return mode, cursor_x, cursor_y, scroll_offset

def save_file(text, filename="output.txt"):
    with open(filename, 'w') as f:
        f.write("\n".join(text))

def execute_user_code(content, stdscr):
    stdscr.clear()  # Limpa a tela para exibir o resultado
    code = "\n".join(content)  # Junta o conteúdo do arquivo como um único código
    try:
        # Tenta executar o código usando o lexer e parser fornecidos
        tokens = lexer(code)
        parser = Parser(tokens)
        result = parser.parse()
        stdscr.addstr("Resultado da execução:\n", curses.color_pair(2))  # Mensagem de sucesso
        stdscr.addstr(str(result) + "\n", curses.color_pair(3))  # Exibe o resultado
    except Exception as e:
        # Exibe a mensagem de erro caso a execução falhe
        stdscr.addstr("Erro ao executar o código:\n", curses.color_pair(1))
        stdscr.addstr(str(e) + "\n", curses.color_pair(1))
    stdscr.addstr("\nPressione qualquer tecla para voltar ao editor...", curses.color_pair(2))
    stdscr.refresh()  # Atualiza a tela para refletir as mudanças
    stdscr.getch()  # Aguarda que o usuário pressione uma tecla para continuar


def initialize_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # Palavras-chave
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Normal (Texto Padrão)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Tab Ativa e Símbolos Especiais
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Números das Linhas
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Operadores
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Números (Roxo)
    curses.init_pair (7, curses.COLOR_CYAN , curses.COLOR_BLACK)

# Operadores e símbolos especiais
SPECIAL_SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
}

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
}

# Palavras-chave
KEYWORDS = [
    "def", "class", "if", "else", "elif", "for", "while", "return", "import", 
    "from", "as", "with", "try", "except", "finally", "pass"
]

# Padrões de token
TOKEN_PATTERNS = {
    "KEYWORD": re.compile(r'\b(?:' + '|'.join(KEYWORDS) + r')\b'),  # Palavras-chave
    "NUMBER": re.compile(r'\b\d+\b'),  # Números
    "SPECIAL_SYMBOL": re.compile(r'|'.join(re.escape(sym) for sym in SPECIAL_SYMBOLS.keys())),
    "OPERATOR": re.compile(r'|'.join(re.escape(op) for op in OPERATORS.keys())),
    "LET": re.compile(r'\blet\b'),  # Palavra 'let'
}

# Função para aplicar o esquema de cores
def apply_color_scheme(stdscr, y, x, line, width):
    """
    Aplica o esquema de cores na linha com base nos padrões de tokens.
    """
    pos = 0
    while pos < len(line):
        # Checa os padrões definidos para tokens
        for token_type, pattern in TOKEN_PATTERNS.items():
            match = pattern.match(line, pos)
            if match:
                token = match.group(0)
                color_pair = {
                    "KEYWORD": curses.color_pair(1),      # Palavras-chave em vermelho
                    "NUMBER": curses.color_pair(6),       # Números em roxo
                    "SPECIAL_SYMBOL": curses.color_pair(3), # Símbolos especiais em magenta
                    "OPERATOR": curses.color_pair(5),     # Operadores em amarelo
                    "LET": curses.color_pair(7)
                }.get(token_type, curses.color_pair(2))  # Cor padrão
                stdscr.addstr(y, x + pos, token, color_pair)
                pos += len(token)
                break
        else:
            # Caracter não identificado como token, renderiza com cor padrão
            stdscr.addch(y, x + pos, line[pos], curses.color_pair(2))
            pos += 1

def display_line_numbers(stdscr, y, width, line_number):
    stdscr.addstr(y, 0, f"{line_number:3} ", curses.color_pair(4))  # Alinhado à esquerda

def main(stdscr):
    curses.curs_set(1)
    initialize_colors()

    cursor_x, cursor_y = 0, 0
    files = [{"name": "untitled.txt", "content": [""]}]
    current_file_index = 0
    scroll_offset = 0
    mode = "VIEWER"
    command_text = ""

    def display_text():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_height = height - 3
        current_file = files[current_file_index]
        text = current_file["content"]
        for i in range(visible_height):
            line_index = i + scroll_offset
            if line_index >= len(text):
                break
            display_line_numbers(stdscr, i, width, line_index + 1)  # Números de linhas
            apply_color_scheme(stdscr, i, 4, text[line_index], width - 4)  # Cores
        display_menu(stdscr, mode, command_text, files, current_file_index)
        cursor_screen_y = cursor_y - scroll_offset
        if 0 <= cursor_screen_y < visible_height:
            stdscr.move(cursor_screen_y, cursor_x + 4)  # Ajustar o cursor para após os números
        stdscr.refresh()

    while True:
        display_text()
        key = stdscr.getch()
        current_file = files[current_file_index]
        text = current_file["content"]

        if mode == "VIEWER":
            mode, command_text, cursor_x, cursor_y, scroll_offset = handle_viewer_mode(
                key, cursor_x, cursor_y, scroll_offset, text, command_text
            )
        elif mode == "COMMAND":
            mode, command_text, should_exit, files, current_file_index = handle_command_mode(
                key, command_text, files, current_file_index, stdscr
            )
            if should_exit:
                break
        elif mode == "EDIT":
            mode, cursor_x, cursor_y, scroll_offset = handle_edit_mode(
                key, cursor_x, cursor_y, scroll_offset, text
            )

curses.wrapper(main)
