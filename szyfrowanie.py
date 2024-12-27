# Funkcja do obsługi kolejki priorytetowej
def priority_queue():
    queue = []

    def push(item):
        queue.append(item)
        queue.sort(key=lambda x: x[1])  # Sortuj rosnąco według częstotliwości

    def pop():
        return queue.pop(0)

    def __len__():
        return len(queue)

    return {"push": push, "pop": pop, "__len__": __len__}


# Budowanie drzewa Huffmana
def build_huffman_tree(text):
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    # Tworzenie kolejki priorytetowej
    pq = priority_queue()
    for char, freq in frequency.items():
        pq["push"]([char, freq, None, None])  # [znak, częstotliwość, lewe dziecko, prawe dziecko]

    # Budowanie drzewa
    while pq["__len__"]() > 1:
        left = pq["pop"]()
        right = pq["pop"]()
        new_node = [None, left[1] + right[1], left, right]
        pq["push"](new_node)

    return pq["pop"]()


# Budowanie kodów Huffmana
def build_codes(node, prefix, codebook):
    if node[0] is not None:
        codebook[node[0]] = prefix
    else:
        build_codes(node[2], prefix + "0", codebook)
        build_codes(node[3], prefix + "1", codebook)


# Kodowanie tekstu
def encode_text(text, codebook):
    return ''.join(codebook[char] for char in text)


# Zapis zakodowanego pliku w formacie tekstowym
def save_encoded_file(encoded_text, codebook, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(str(codebook) + "\n")  # Nagłówek
        file.write(encoded_text)          # Zakodowany tekst


# Funkcja kodowania Huffmana
def huffman_encode(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    tree = build_huffman_tree(text)
    codebook = {}
    build_codes(tree, "", codebook)

    encoded_text = encode_text(text, codebook)
    save_encoded_file(encoded_text, codebook, output_file)

# Przykład użycia
huffman_encode("input.txt", "encoded.txt")