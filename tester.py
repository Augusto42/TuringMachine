import json
import os
import subprocess

# Define os casos de teste
test_cases = [
    {
        "description": "Máquina de Turing Básica (Sem Backtracking Necessário)",
        "json": {
            "mt": [
                ["e1", "e2", "e3"],
                ["a", "b"],
                ["[", "_", "a", "b"],
                "[",
                "_",
                [
                    ["e1", "a", "e2", "b", ">"],
                    ["e2", "b", "e3", "a", "<"]
                ],
                "e1",
                ["e3"]
            ]
        },
        "input_word": "a",
        "expected_output": "Sim"
    },
    {
        "description": "Máquina de Turing com Múltiplas Transições Válidas (Necessário Backtracking)",
        "json": {
            "mt": [
                ["e1", "e2", "e3", "e4", "e5"],
                ["a", "b", "c"],
                ["[", "_", "a", "b", "c"],
                "[",
                "_",
                [
                    ["e1", "a", "e2", "b", ">"],
                    ["e1", "a", "e3", "c", ">"],
                    ["e2", "b", "e4", "b", ">"],
                    ["e3", "c", "e5", "c", "<"],
                    ["e4", "b", "e5", "c", ">"]
                ],
                "e1",
                ["e5"]
            ]
        },
        "input_word": "ab",
        "expected_output": "Sim"
    },
    {
        "description": "Máquina de Turing que Rejeita a Palavra (Sem Estado Final Alcançado)",
        "json": {
            "mt": [
                ["e1", "e2", "e3"],
                ["a", "b"],
                ["[", "_", "a", "b"],
                "[",
                "_",
                [
                    ["e1", "a", "e2", "b", ">"],
                    ["e2", "b", "e3", "b", "<"]
                ],
                "e1",
                ["e3"]
            ]
        },
        "input_word": "aa",
        "expected_output": "Não"
    },
    {
        "description": "Máquina de Turing com Ciclo Infinito (Backtracking para Evitar Ciclo)",
        "json": {
            "mt": [
                ["e1", "e2", "e3", "e4"],
                ["a", "b"],
                ["[", "_", "a", "b"],
                "[",
                "_",
                [
                    ["e1", "a", "e2", "b", ">"],
                    ["e2", "b", "e1", "a", "<"],
                    ["e1", "b", "e3", "b", ">"]
                ],
                "e1",
                ["e3"]
            ]
        },
        "input_word": "ab",
        "expected_output": "Sim"
    },
    {
        "description": "Máquina de Turing que Requer Múltiplos Backtracking para Alcançar o Estado Final",
        "json": {
            "mt": [
                ["e1", "e2", "e3", "e4", "e5", "e6"],
                ["a", "b", "c"],
                ["[", "_", "a", "b", "c"],
                "[",
                "_",
                [
                    ["e1", "a", "e2", "b", ">"],
                    ["e1", "a", "e3", "c", ">"],
                    ["e2", "b", "e4", "b", ">"],
                    ["e3", "c", "e5", "c", "<"],
                    ["e4", "b", "e1", "a", "<"],
                    ["e5", "c", "e6", "c", "<"]
                ],
                "e1",
                ["e6"]
            ]
        },
        "input_word": "abc",
        "expected_output": "Sim"
    }
]

# Nome do arquivo JSON usado pelo código original
json_file = "mt.json"

# Função para escrever o JSON em um arquivo
def write_json_to_file(json_data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# Função para executar o código e capturar a saída
def run_turing_machine(input_word):
    result = subprocess.run(['python', 'mt.py', json_file, input_word], capture_output=True, text=True)
    return result.stdout.strip()

# Executa os testes
for test in test_cases:
    print(f"Executando teste: {test['description']}")
    # Escreve o JSON do teste no arquivo
    write_json_to_file(test['json'], json_file)
    # Executa o código com a palavra de entrada
    output = run_turing_machine(test['input_word'])
    # Verifica se a saída corresponde ao esperado
    if output == test['expected_output']:
        print("Resultado: PASSOU")
    else:
        print(f"Resultado: FALHOU (Esperado: {test['expected_output']}, Obtido: {output})")
    print()

# Limpa o arquivo JSON ao final
os.remove(json_file)
