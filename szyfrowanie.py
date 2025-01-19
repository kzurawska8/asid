import pickle

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def insert(self, priority, value):
        self.queue.append((priority, value))

    def pop(self):
        if self.is_empty():
            return None
        
        highest_priority_index = 0
        for i in range(1, len(self.queue)):
            if self.queue[i][0] < self.queue[highest_priority_index][0]:
                highest_priority_index = i
        
        return self.queue.pop(highest_priority_index)

def build_huffman_tree(text):
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    pq = PriorityQueue()
    for char, freq in frequency.items():
        pq.insert(freq, [char, freq, None, None])

    while len(pq.queue) > 1:
        left = pq.pop()[1]
        right = pq.pop()[1]
        new_node = [None, left[1] + right[1], left, right]
        pq.insert(new_node[1], new_node)

    return pq.pop()[1]

def build_codes(node, prefix, codebook):
    if node[0] is not None:
        codebook[node[0]] = prefix
    else:
        build_codes(node[2], prefix + "0", codebook)
        build_codes(node[3], prefix + "1", codebook)

def encode_text(text, codebook):
    return ''.join(codebook[char] for char in text)

def save_encoded_file(encoded_text, codebook, output_file):
    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_array.append(int(byte, 2))

    with open(output_file, "wb") as file:
        pickle.dump({"codebook": codebook, "encoded_text": byte_array}, file)

def huffman_encode(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    tree = build_huffman_tree(text)
    codebook = {}
    build_codes(tree, "", codebook)

    encoded_text = encode_text(text, codebook)
    save_encoded_file(encoded_text, codebook, output_file)

huffman_encode("input.txt", "encoded.bin")