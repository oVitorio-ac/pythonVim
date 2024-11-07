import curses

def main(stdscr):
    # Configurações iniciais
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    line_bar_width = 5
    cursor_x, cursor_y = 0, 0
    text = [""]
    scroll_offset = 0
    command_mode = False
    command_text = ""
    mode = "VIEWER"  # Inicializando no modo VIEWER

    # Função para exibir o texto com a barra de linha
    def display_text():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_height = height - 2  # Desconta o rodapé

        # Exibe o texto com números de linha
        for i in range(visible_height):
            line_index = i + scroll_offset
            if line_index >= len(text):
                break
            line_number = str(line_index + 1).rjust(line_bar_width - 1) + " "
            stdscr.addstr(i, 0, line_number[:line_bar_width])
            stdscr.addstr(i, line_bar_width, text[line_index][:width - line_bar_width - 2])

        # Barra de rolagem
        if len(text) > visible_height:
            scrollbar_position = int((scroll_offset / max(len(text) - visible_height, 1)) * (visible_height - 1))
            for i in range(visible_height):
                if i == scrollbar_position:
                    stdscr.addstr(i, width - 1, '|')
                else:
                    stdscr.addstr(i, width - 1, ' ')

        # Rodapé com modo e comandos
        stdscr.addstr(height - 1, 0, f"Mode: {mode} | Commands: :save :kill :edit", curses.A_REVERSE)

        # Mostra o comando em modo VIEWER
        if command_mode:
            stdscr.addstr(height - 2, 0, ":" + command_text)

        # Atualiza a posição do cursor com a rolagem e barra de linha
        cursor_screen_y = cursor_y - scroll_offset
        if 0 <= cursor_screen_y < visible_height:
            stdscr.move(cursor_screen_y, cursor_x + line_bar_width)
        stdscr.refresh()

    # Função para salvar o texto em um arquivo
    def save_file(filename="output.txt"):
        with open(filename, 'w') as f:
            f.write("\n".join(text))

    while True:
        height, width = stdscr.getmaxyx()
        display_text()
        key = stdscr.getch()

        # Modo VIEWER para comando e navegação
        if mode == "VIEWER":
            if key == 27:  # ESC para entrar no modo de comando
                mode = "COMMAND"
                command_mode = True
                command_text = ""
            elif key == curses.KEY_BACKSPACE or key in [127, 8]:  # Apaga o último caractere
                command_text = command_text[:-1]
            elif 32 <= key <= 126:  # Adiciona caracteres ao comando
                command_text += chr(key)
            # Navegação no modo VIEWER
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

        # Modo de comando
        elif mode == "COMMAND":
            if key == 27:  # ESC para voltar ao modo VIEWER
                mode = "VIEWER"
                command_mode = False  # Desativa o modo de comando
                command_text = ""
            elif key == 10:  # Enter para executar o comando
                if command_text == "save":
                    save_file()
                elif command_text == "kill":
                    break
                elif command_text == "edit":
                    mode = "EDIT"  # Vai para o modo de edição
                command_mode = False
                command_text = ""
            elif key == curses.KEY_BACKSPACE or key in [127, 8]:  # Apaga o último caractere
                command_text = command_text[:-1]
            elif 32 <= key <= 126:  # Adiciona caracteres ao comando
                command_text += chr(key)
            elif key == ord(' '):  # Adiciona espaços ao comando
                command_text += ' '
            elif key == ord(':'):  # O ":" permanece no início do comando
                command_text = ":" + command_text[1:]

        # Modo de edição de texto
        elif mode == "EDIT":
            if key == 27:  # ESC para voltar ao modo VIEWER
                mode = "VIEWER"
                command_mode = False  # Encerra o modo de comando
                command_text = ""
            elif key == curses.KEY_UP:
                if cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = min(cursor_x, len(text[cursor_y]))
                if cursor_y < scroll_offset:
                    scroll_offset -= 1
            elif key == curses.KEY_DOWN:
                if cursor_y < len(text) - 1:
                    cursor_y += 1
                    cursor_x = min(cursor_x, len(text[cursor_y]))
                if cursor_y >= scroll_offset + (height - 2):
                    scroll_offset += 1
            elif key == curses.KEY_LEFT:
                if cursor_x > 0:
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_x = len(text[cursor_y - 1])
                    text[cursor_y - 1] += text.pop(cursor_y)
                    cursor_y -= 1
                    if cursor_y < scroll_offset:
                        scroll_offset -= 1
            elif key == curses.KEY_RIGHT:
                if cursor_x < len(text[cursor_y]):
                    cursor_x += 1
                elif cursor_y < len(text) - 1:
                    cursor_y += 1
                    cursor_x = 0
            elif key == ord('\n'):
                text.insert(cursor_y + 1, text[cursor_y][cursor_x:])
                text[cursor_y] = text[cursor_y][:cursor_x]
                cursor_y += 1
                cursor_x = 0
                if cursor_y >= scroll_offset + (height - 2):
                    scroll_offset += 1
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if cursor_x > 0:
                    text[cursor_y] = text[cursor_y][:cursor_x - 1] + text[cursor_y][cursor_x:]
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_x = len(text[cursor_y - 1])
                    text[cursor_y - 1] += text.pop(cursor_y)
                    cursor_y -= 1
                    if cursor_y < scroll_offset:
                        scroll_offset -= 1
            elif key == ord('\t'):  # Insere espaços ao invés de Tab
                tab_spaces = "    "
                text[cursor_y] = text[cursor_y][:cursor_x] + tab_spaces + text[cursor_y][cursor_x:]
                cursor_x += len(tab_spaces)
            else:
                text[cursor_y] = text[cursor_y][:cursor_x] + chr(key) + text[cursor_y][cursor_x:]
                cursor_x += 1

curses.wrapper(main)
