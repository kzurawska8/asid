# moduł, umożliwia serializację i deserializację obiektów, którą używam do zapisu pliku binarnie
import pickle

def load_encoded_file(input_file):
    # otwieranie pliku binarnego z zakodowanymi danymi w trybie odczytu binarnego
    with open(input_file, "rb") as file:
        # ładowanie zawartości pliku przy użyciu 'pickle'
        data = pickle.load(file)
    # najpierw wyciągamy słownik kodów z danych w pliku
    codebook = data["codebook"]
    # przekształcamy zapisane bajty na ciąg binarny
    encoded_text = ''.join(f"{byte:08b}" for byte in data["encoded_text"])
    return codebook, encoded_text

def decode_text(encoded_text, codebook):
    # tworzymy odwrotny słownik kodów - mapowanie kodu binarnego na znak
    # key to ten kod składający się z 0 i 1 a value to znak np. 'a'
    reverse_codebook = {v: k for k, v in codebook.items()}
    # zmienna na zdekodowany tekst
    decoded_text = ""
    # zmienna na tymczasowe przechowywanie fragmentu kodu binarnego
    temp_code = ""

    # przechodzimy przez każdy bit kodu
    for bit in encoded_text:
        # dodajemy bit do tymczasowej zmiennej
        temp_code += bit
        # sprawdzamy czy tymczasowa zmienna zawiera kod, który znajduje się w odwróconym słowniku
        if temp_code in reverse_codebook:
            # jeśli tak, dodajemy znak do zdekodowanego tekstu
            decoded_text += reverse_codebook[temp_code]
            # reset tymczasowej zmiennej
            temp_code = ""

    return decoded_text

# funkcja obsugująca wczytywanie zakodowanego pliku i implementacji deszyfrowania
def huffman_decode(input_file, output_file):
    codebook, encoded_text = load_encoded_file(input_file)

    decoded_text = decode_text(encoded_text, codebook)

    # plik wyjściowy jest otwierany w trybie zapisu
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)

huffman_decode("encoded.bin", "decoded.txt")