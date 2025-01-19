import pickle

def load_encoded_file(input_file):
    with open(input_file, "rb") as file:
        data = pickle.load(file)
    codebook = data["codebook"]
    encoded_text = ''.join(f"{byte:08b}" for byte in data["encoded_text"])
    return codebook, encoded_text

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

def huffman_decode(input_file, output_file):
    codebook, encoded_text = load_encoded_file(input_file)

    decoded_text = decode_text(encoded_text, codebook)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)

huffman_decode("encoded.bin", "decoded.txt")