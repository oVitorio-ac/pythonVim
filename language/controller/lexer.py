import re
from language.model.keywords import KEYWORDS, SPECIAL_SYMBOLS, OPERATORS, TOKEN_TYPES
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code

    def is_keyword(self, word):
        return KEYWORDS.get(word)  # Verifica se a palavra é uma palavra-chave

    def is_special_symbol(self, char):
        return SPECIAL_SYMBOLS.get(char)  # Verifica se é um símbolo especial

    def tokenize(self):
        tokens = []
        current_index = 0
        while current_index < len(self.source_code):  # Aqui, `self.source_code` deve ser uma string
            char = self.source_code[current_index]

            # Ignorar espaços em branco
            if re.match(TOKEN_TYPES["WHITESPACE"], char):
                current_index += 1
                continue

            # Verificar se é um número
            match_number = re.match(TOKEN_TYPES["NUMBER"], self.source_code[current_index:])
            if match_number:
                tokens.append(("NUMBER", match_number.group()))
                current_index += len(match_number.group())
                continue

            # Verificar se é um identificador ou palavra-chave
            match_identifier = re.match(TOKEN_TYPES["IDENTIFIER"], self.source_code[current_index:])
            if match_identifier:
                word = match_identifier.group()
                # Verificar se é uma palavra-chave
                keyword = self.is_keyword(word)
                if keyword:
                    tokens.append((keyword, word))
                else:
                    tokens.append(("IDENTIFIER", word))
                current_index += len(word)
                continue

            # Verificar se é um operador composto (como ==, !=, >=, <=)
            for operator in sorted(OPERATORS.keys(), key=len, reverse=True):  # Ordena para verificar operadores compostos primeiro
                if self.source_code[current_index:current_index + len(operator)] == operator:
                    tokens.append((OPERATORS[operator], operator))
                    current_index += len(operator)
                    print(f"Operador composto encontrado: {operator}")
                    break
            else:
                # Verificar se é um operador simples (como =)
                if char in OPERATORS:
                    tokens.append((OPERATORS[char], char))
                    current_index += 1
                    print(f"Operador simples encontrado: {char}")
                    continue

                # Verificar se é um símbolo especial
                if char in SPECIAL_SYMBOLS:
                    tokens.append((SPECIAL_SYMBOLS[char], char))
                    current_index += 1
                    continue

                # Se nenhum token for encontrado, é um caractere inválido
                raise ValueError(f"Caractere inválido: {char}")

        return tokens
