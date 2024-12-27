# Wczytywanie zakodowanego pliku tekstowego
def load_encoded_file(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        codebook = eval(file.readline().strip())
        encoded_text = file.read().strip()
    return codebook, encoded_text


# Dekodowanie tekstu
def decode_text(encoded_text, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_text = ""
    temp_code = ""

    for bit in encoded_text:
        temp_code += bit
        if temp_code in reverse_codebook:
            decoded_text += reverse_codebook[temp_code]
            temp_code = ""

    return decoded_text


# Funkcja dekodowania Huffmana
def huffman_decode(input_file, output_file):
    codebook, encoded_text = load_encoded_file(input_file)

    decoded_text = decode_text(encoded_text, codebook)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)

# Dekodowanie
huffman_decode("encoded.txt", "decoded.txt")