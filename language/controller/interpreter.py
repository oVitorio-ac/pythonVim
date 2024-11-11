# Contexto para armazenar variáveis
context = {}

def interpret_node(node):
    if node['type'] == 'var_declaration':
        # Declaração de variável
        var_name = node['name']
        value = int(node['value'])  # Supondo que o valor seja sempre numérico
        context[var_name] = value

    elif node['type'] == 'condition_statement':
        # Condição
        left_operand = context.get(node['condition']['left_operand'])
        right_operand = int(node['condition']['right_operand'])
        operator = node['condition']['operator']

        # Avalia a condição
        if operator == '==' and left_operand == right_operand:
            # Executa o corpo se a condição for verdadeira
            for stmt in node['body']:
                interpret_node(stmt)
        elif node['alternative']:
            # Executa o bloco "alternative" se a condição for falsa
            for stmt in node['alternative']:
                interpret_node(stmt)

    elif node['type'] == 'output_statement':
        # Saída (imprime o valor)
        value = context.get(node['value'], node['value'])
        print(value)

# Exemplo de execução
ast = [
    {'type': 'var_declaration', 'name': 'x', 'value': '5'},
    {
        'type': 'condition_statement',
        'condition': {'left_operand': 'x', 'operator': '==', 'right_operand': '5'},
        'body': [{'type': 'output_statement', 'value': 'x'}],
        'alternative': [{'type': 'output_statement', 'value': '0'}]
    },
    {'type': 'output_statement', 'value': '0'}
]

for node in ast:
    interpret_node(node)
