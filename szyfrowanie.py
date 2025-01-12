# moduł, umożliwia serializację i deserializację obiektów, którą używam do zapisu pliku binarnie
import pickle

class PriorityQueue:
    # pusta kolejka
    def __init__(self):
        self.queue = []

    # czy kolejka jest pusta
    def is_empty(self):
        return len(self.queue) == 0

    # dodawanie elementu z priorytetem
    def insert(self, priority, value):
        self.queue.append((priority, value))

    def pop(self):
        if self.is_empty():
            return None
        
        # ustawiamy element z "najwyższym priorytetem"
        highest_priority_index = 0
        # znajdowanie elementu z najniższym priorytetem
        for i in range(1, len(self.queue)):
            if self.queue[i][0] < self.queue[highest_priority_index][0]:
                highest_priority_index = i
        
        # usuwanie i zwracanie elementu z najwyższym priorytetem
        return self.queue.pop(highest_priority_index)

def build_huffman_tree(text):
    # słownik, który będzie przechowywał częstotliwość występowania znaku w tekście
    frequency = {}
    # zliczanie tego występowania znaku
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    pq = PriorityQueue()
    # wstawianie znaków jako węzły-liście drzewa Huffmana, liście nie mają dzieci dlatego zostaje ustawione None None
    for char, freq in frequency.items():
        pq.insert(freq, [char, freq, None, None])

    while len(pq.queue) > 1:
        # element z najinższym priorytetem zostaje lewym potomkiem
        left = pq.pop()[1]
        # element z następnym najniższym priorytetem zostaje prawym potomkiem
        right = pq.pop()[1]
        # nowy węzeł wewnętrzny z sumą priorytetów, nie reprezentuje żadnego znaku dlatego None, dzieci mogą być liścmi lub innymi węzłami wewnętrznymi
        new_node = [None, left[1] + right[1], left, right]
        # dodanie węzła do kolejki, częstotliwość i pełna struktura węzła
        pq.insert(new_node[1], new_node)

    # zwracamy korzeń drzewa, bez priorytetu
    return pq.pop()[1]

def build_codes(node, prefix, codebook):
    # jeśli node_value nie jest None - czyli jest liściem
    if node[0] is not None:
        # dodawanie kodu binarnego dla znaku do słownika kodów
        codebook[node[0]] = prefix
    else:
        # rekurencyjne budowanie kodu dla lewego poddrzewa
        build_codes(node[2], prefix + "0", codebook)
        # rekurencyjne budowanie kodu dla prawego poddrzewa
        build_codes(node[3], prefix + "1", codebook)

def encode_text(text, codebook):
    # korzystając ze zbudowanego słownika kodowanie tekstu
    return ''.join(codebook[char] for char in text)

def save_encoded_file(encoded_text, codebook, output_file):
    # pusta tablica bajtów
    byte_array = bytearray()
    # iteracja przez tekst co 8 znaków
    for i in range(0, len(encoded_text), 8):
        # pobieranie kolejnych 8 bitów z zakodowanego tekstu
        byte = encoded_text[i:i+8]
        # konwersja 8-bitowego ciągu na liczbę całkowitą i dodawanie do tablicy bajtów
        byte_array.append(int(byte, 2))

    with open(output_file, "wb") as file:
        # zapisywanie słownika kodów i zakodowanego tekstu do pliku
        pickle.dump({"codebook": codebook, "encoded_text": byte_array}, file)

# funkcja obsugująca wczytywanie pliku wejściowego i implementacji szyfrowania
def huffman_encode(input_file, output_file):
    # odczytywanie tekstu z pliku wejściowego
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    tree = build_huffman_tree(text)
    codebook = {}
    build_codes(tree, "", codebook)

    encoded_text = encode_text(text, codebook)
    save_encoded_file(encoded_text, codebook, output_file)

huffman_encode("input.txt", "encoded.bin")