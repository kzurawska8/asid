import pickle

def heapify(heap, i, heap_size):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and heap[left][0] < heap[smallest][0]:
        smallest = left
    if right < heap_size and heap[right][0] < heap[smallest][0]:
        smallest = right

    if smallest != i:
        heap[i], heap[smallest] = heap[smallest], heap[i]
        heapify(heap, smallest, heap_size)

def build_min_heap(heap):
    for i in range(len(heap) // 2 - 1, -1, -1):
        heapify(heap, i, len(heap))

def heap_pop(heap):
    if not heap:
        return None

    root = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    heapify(heap, 0, len(heap))

    return root

def heap_push(heap, node):
    heap.append(node)
    i = len(heap) - 1
    parent = (i - 1) // 2

    while i > 0 and heap[i][0] < heap[parent][0]:
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent
        parent = (i - 1) // 2

def build_huffman_tree(text):
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    heap = [(freq, [char, freq, None, None]) for char, freq in frequency.items()]
    build_min_heap(heap)

    while len(heap) > 1:
        left = heap_pop(heap)[1]
        right = heap_pop(heap)[1]
        new_node = [None, left[1] + right[1], left, right]
        heap_push(heap, (new_node[1], new_node))

    return heap_pop(heap)[1]

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