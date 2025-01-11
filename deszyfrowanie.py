import pickle  # Importuje moduł `pickle`, który umożliwia serializację i deserializację obiektów w Pythonie.

def load_encoded_file(input_file):
    with open(input_file, "rb") as file:  # Otwiera plik binarny z zakodowanymi danymi w trybie odczytu binarnego.
        data = pickle.load(file)  # Ładuje zawartość pliku (słownik) przy użyciu `pickle`.
    codebook = data["codebook"]  # Wyciąga słownik kodów Huffmana z danych.
    encoded_text = ''.join(f"{byte:08b}" for byte in data["encoded_text"])  
    # Przekształca zapisane bajty na ciąg binarny (po 8 bitów na bajt).
    return codebook, encoded_text  # Zwraca słownik kodów i ciąg zakodowanego tekstu.

def decode_text(encoded_text, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}  
    # Tworzy odwrotny słownik kodów (mapuje kod binarny na znak).
    decoded_text = ""  # Inicjalizuje pusty ciąg na zdekodowany tekst.
    temp_code = ""  # Tymczasowy ciąg przechowujący fragmenty kodu binarnego.

    for bit in encoded_text:  # Iteruje przez każdy bit zakodowanego tekstu.
        temp_code += bit  # Dodaje bit do tymczasowego kodu.
        if temp_code in reverse_codebook:  # Sprawdza, czy tymczasowy kod znajduje się w odwrotnym słowniku.
            decoded_text += reverse_codebook[temp_code]  
            # Jeśli tak, dodaje odpowiadający znak do zdekodowanego tekstu.
            temp_code = ""  # Resetuje tymczasowy kod.

    return decoded_text  # Zwraca zdekodowany tekst.

def huffman_decode(input_file, output_file):
    codebook, encoded_text = load_encoded_file(input_file)  
    # Ładuje słownik kodów i ciąg zakodowanego tekstu z pliku wejściowego.

    decoded_text = decode_text(encoded_text, codebook)  
    # Dekoduje zakodowany tekst na podstawie słownika kodów.

    with open(output_file, "w", encoding="utf-8") as file:  
        # Otwiera plik wyjściowy w trybie zapisu z kodowaniem UTF-8.
        file.write(decoded_text)  # Zapisuje zdekodowany tekst do pliku.

huffman_decode("encoded.bin", "decoded.txt")  
# Wywołuje funkcję dekodowania Huffmana, odczytując dane z "encoded.bin" i zapisując wynik do "decoded.txt".