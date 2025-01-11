import pickle  # Importuje moduł `pickle`, który umożliwia serializację i deserializację obiektów w Pythonie.

class PriorityQueue:
    def __init__(self):
        self.queue = []  # Inicjalizuje pustą kolejkę priorytetową.

    def is_empty(self):
        return len(self.queue) == 0  # Sprawdza, czy kolejka jest pusta.

    def insert(self, priority, value):
        self.queue.append((priority, value))  # Dodaje element z określonym priorytetem do kolejki.

    def pop(self):
        if self.is_empty():
            return None  # Zwraca `None`, jeśli kolejka jest pusta.
        
        highest_priority_index = 0  # Inicjalizuje indeks elementu z najwyższym priorytetem.
        for i in range(1, len(self.queue)):
            if self.queue[i][0] < self.queue[highest_priority_index][0]:  # Znajduje element o najniższym priorytecie.
                highest_priority_index = i
        
        return self.queue.pop(highest_priority_index)  # Usuwa i zwraca element z najwyższym priorytetem.

    def peek(self):
        if self.is_empty():
            return None  # Zwraca `None`, jeśli kolejka jest pusta.
        
        highest_priority_index = 0  # Inicjalizuje indeks elementu z najwyższym priorytetem.
        for i in range(1, len(self.queue)):
            if self.queue[i][0] < self.queue[highest_priority_index][0]:  # Znajduje element o najniższym priorytecie.
                highest_priority_index = i
        
        return self.queue[highest_priority_index]  # Zwraca element z najwyższym priorytetem bez usuwania go.

def build_huffman_tree(text):
    frequency = {}  # Tworzy słownik przechowujący częstotliwości występowania znaków w tekście.
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1  # Zlicza wystąpienia każdego znaku w tekście.

    pq = PriorityQueue()  # Inicjalizuje kolejkę priorytetową.
    for char, freq in frequency.items():
        pq.insert(freq, [char, freq, None, None])  # Wstawia znaki jako liście drzewa Huffmana.

    while len(pq.queue) > 1:
        left = pq.pop()[1]  # Pobiera element z najniższym priorytetem jako lewego potomka.
        right = pq.pop()[1]  # Pobiera element z następnym najniższym priorytetem jako prawego potomka.
        new_node = [None, left[1] + right[1], left, right]  # Tworzy nowy węzeł z sumą priorytetów.
        pq.insert(new_node[1], new_node)  # Dodaje nowy węzeł do kolejki.

    return pq.pop()[1]  # Zwraca korzeń drzewa Huffmana.

def build_codes(node, prefix, codebook):
    if node[0] is not None:  # Sprawdza, czy węzeł jest liściem.
        codebook[node[0]] = prefix  # Dodaje kod binarny dla znaku do słownika kodów.
    else:
        build_codes(node[2], prefix + "0", codebook)  # Rekurencyjnie buduje kod dla lewego poddrzewa.
        build_codes(node[3], prefix + "1", codebook)  # Rekurencyjnie buduje kod dla prawego poddrzewa.

def encode_text(text, codebook):
    return ''.join(codebook[char] for char in text)  # Koduje tekst na podstawie słownika kodów.

def save_encoded_file(encoded_text, codebook, output_file):
    byte_array = bytearray()  # Tworzy pustą tablicę bajtów.
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]  # Bierze kolejne 8 bitów z zakodowanego tekstu.
        byte_array.append(int(byte, 2))  # Konwertuje 8-bitowy ciąg na liczbę całkowitą i dodaje do tablicy bajtów.

    with open(output_file, "wb") as file:
        pickle.dump({"codebook": codebook, "encoded_text": byte_array}, file)  # Zapisuje słownik kodów i zakodowany tekst do pliku.

def huffman_encode(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()  # Odczytuje tekst z pliku wejściowego.

    tree = build_huffman_tree(text)  # Buduje drzewo Huffmana na podstawie tekstu.
    codebook = {}  # Tworzy pusty słownik na kody Huffmana.
    build_codes(tree, "", codebook)  # Wypełnia słownik kodów na podstawie drzewa Huffmana.

    encoded_text = encode_text(text, codebook)  # Koduje tekst na ciąg binarny.
    save_encoded_file(encoded_text, codebook, output_file)  # Zapisuje zakodowany tekst i słownik kodów do pliku binarnego.

huffman_encode("input.txt", "encoded.bin")  # Wywołuje funkcję Huffman Encode na pliku wejściowym "input.txt".