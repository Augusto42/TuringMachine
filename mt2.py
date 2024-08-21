import json
import sys
from copy import deepcopy

class TuringMachine:
    def __init__(self, mt_spec):
        self.states = mt_spec["mt"][0]
        self.input_alphabet = mt_spec["mt"][1]
        self.tape_alphabet = mt_spec["mt"][2]
        self.start_symbol = mt_spec["mt"][3]
        self.blank_symbol = mt_spec["mt"][4]
        self.transitions = mt_spec["mt"][5]
        self.initial_state = mt_spec["mt"][6]
        self.final_states = mt_spec["mt"][7]
        self.current_state = self.initial_state
        self.tape = []
        self.head_position = 1  # Inicializa após o símbolo de início
        self.visited_states = set()  # Conjunto para armazenar estados visitados
        self.stack = []  # Pilha para armazenar estados anteriores (backtracking)

    def initialize_tape(self, input_word):
        self.tape = list(input_word)
        if not self.tape:
            self.tape.append(self.blank_symbol)
        self.tape.insert(0, self.start_symbol)  # Insere o símbolo de início da fita
        self.head_position = 1  # Cabeçote começa no primeiro símbolo da palavra

    def step(self):
        state_key = (self.current_state, self.head_position, ''.join(self.tape))
        if state_key in self.visited_states:
            return False  # Evitar revisitar o mesmo estado repetidamente

        self.visited_states.add(state_key)
        current_symbol = self.tape[self.head_position]
        possible_transitions = [t for t in self.transitions if t[0] == self.current_state and t[1] == current_symbol]

        if not possible_transitions:
            if self.stack:
                # Restaura o estado anterior
                self.current_state, self.tape, self.head_position = self.stack.pop()
                print(f"Reiniciando do estado {self.current_state} com fita {''.join(self.tape)}")
                self.step()
                return True
            else:
                print(f"Sem transições possíveis para o estado {self.current_state} e símbolo {current_symbol}")
                return False
        
        # Armazena o estado atual na pilha antes de escolher uma transição
        self.stack.append((self.current_state, deepcopy(self.tape), self.head_position))

        for transition in possible_transitions:
            current_symbol = self.tape[self.head_position]
            if transition[1] != current_symbol:
                continue
            print(f"Estado atual: {self.current_state}, Símbolo atual: {current_symbol}")
            print(f"Executando transição: {transition}")
            new_state, new_symbol, direction = transition[2], transition[3], transition[4]
            self.tape[self.head_position] = new_symbol
            self.current_state = new_state
            print(f"Novo estado: {self.current_state}, Novo símbolo na fita: {new_symbol}, Direção: {direction}")

            if direction == '>':
                self.head_position += 1
                if self.head_position >= len(self.tape):
                    self.tape.append(self.blank_symbol)
            elif direction == '<':
                self.head_position -= 1
                if self.head_position < 0:
                    self.tape.insert(0, self.blank_symbol)
                    self.head_position = 0

            print(f"Fita atual: {''.join(self.tape)}, Posição do cabeçote: {self.head_position}")

            if self.current_state in self.final_states:
                print(f"Estado final {self.current_state} alcançado")
                return True

        return True  # Continua a execução se transições foram realizadas

    def run(self, input_word):
        self.initialize_tape(input_word)
        while True:
            if not self.step():
                return False  # Se nenhuma transição foi encontrada, a palavra não é aceita
            if self.current_state in self.final_states:
                return True  # Encerra quando atingir um estado final


def main(mt_file, input_word):
    with open(mt_file, 'r') as f:
        mt_spec = json.load(f)

    tm = TuringMachine(mt_spec)
    if tm.run(input_word):
        print("Sim")
    else:
        print("Não")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usar: ./mt [MT] [Palavra]")
        sys.exit(1)

    mt_file = sys.argv[1]
    input_word = sys.argv[2]
    main(mt_file, input_word)
