import curses
from config.menu import display_menu, handle_command_mode, handle_viewer_mode, handle_edit_mode
from config.colors import initialize_colors, apply_color_scheme

def main(stdscr):
    # Configurações iniciais
    curses.curs_set(1)
    initialize_colors()

    # Variáveis de controle
    line_bar_width = 5
    cursor_x, cursor_y = 0, 0
    files = [{"name": "untitled.txt", "content": [""]}]  # Cada aba representa um arquivo
    current_file_index = 0  # Aba ativa
    scroll_offset = 0
    mode = "VIEWER"
    command_text = ""

    # Função para exibir o conteúdo do texto
    def display_text():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_height = height - 3  # Ajuste para incluir o cabeçalho do menu

        current_file = files[current_file_index]
        text = current_file["content"]

        # Exibir texto e números de linha
        for i in range(visible_height):
            line_index = i + scroll_offset
            if line_index >= len(text):
                break
            line_number = str(line_index + 1).rjust(line_bar_width - 1) + " "
            stdscr.addstr(i, 0, line_number[:line_bar_width])
            apply_color_scheme(stdscr, i, line_bar_width, text[line_index], width)

        # Exibir o cabeçalho com o nome do projeto e instruções
        display_menu(stdscr, mode, command_text, files, current_file_index)
        
        # Colocar o cursor na posição certa
        cursor_screen_y = cursor_y - scroll_offset
        if 0 <= cursor_screen_y < visible_height:
            stdscr.move(cursor_screen_y, cursor_x + line_bar_width)
        stdscr.refresh()

    # Loop principal do editor
    while True:
        height, width = stdscr.getmaxyx()
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
                key, command_text, files, current_file_index
            )
            if should_exit:
                break
        elif mode == "EDIT":
            mode, cursor_x, cursor_y, scroll_offset = handle_edit_mode(
                key, cursor_x, cursor_y, scroll_offset, text
            )
curses.wrapper(main)
