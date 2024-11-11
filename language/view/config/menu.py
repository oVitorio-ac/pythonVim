import curses

def display_menu(stdscr, mode, command_text, files, current_file_index):
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 2, 0, f"Projeto: Editor de Texto | Use ESC para Comando | Ctrl+N: Novo Arquivo | Ctrl+Tab: Alternar Aba")
    
    # Exibir abas com os nomes dos arquivos
    for i, file in enumerate(files):
        tab_text = f"[{file['name']}] "
        color = curses.color_pair(3) if i == current_file_index else curses.color_pair(2)
        stdscr.addstr(height - 1, i * 15, tab_text, color)
    
    # Exibir o texto de comando no modo COMMAND
    if mode == "COMMAND":
        stdscr.addstr(height - 3, 0, ":" + command_text)

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

def handle_command_mode(key, command_text, files, current_file_index):
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
        # Lógica de backspace
        if cursor_x > 0:
            line = text[cursor_y]
            text[cursor_y] = line[:cursor_x - 1] + line[cursor_x:]
            cursor_x -= 1
        elif cursor_y > 0:
            # Move para a linha anterior se o cursor estiver no início
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
