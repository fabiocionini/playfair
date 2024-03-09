import \
    re
import \
    sys
from string import ascii_lowercase

print("-------------------------------------------------------")
print("Playfair cypher encrypt/decrypt                        ")
print("A Saturday afternoon project by Miranda & Fabio Cionini")
print("09/03/2024                                             ")
print("-------------------------------------------------------")
print(" ")

import signal

def keyboard_interrupt_handler(signal, frame):
    exit(0)


signal.signal(signal.SIGINT, keyboard_interrupt_handler)

def valid_key(string):
    chars = list(string)
    dedup = set(chars)
    return len(string) > 1 and re.match('^[a-z]+$', string) and len(dedup) == len(string) and "j" not in dedup
def create_matrix(string):
    sequence = ''.join(list(string) + [c for c in list(ascii_lowercase) if c not in list(key) and c != 'j'])
    matrix = []
    for r in range(5):
        matrix.append(list(sequence[r*5:r*5+5]))
    # for row in matrix:
    #     print(row)
    return matrix
def get_char_from_matrix(matrix, row, column):
    return matrix[row][column]
def find_in_matrix(matrix, char):
    column_index = None
    row_index = None
    for row_index, row in enumerate(matrix):
        try:
            column_index = row.index(char)
            break
        except ValueError:
            pass
    if column_index is not None:
        return row_index, column_index, row_index * 5 + column_index
    else:
        return None
def find_digraph_in_matrix(matrix, key):
    out = []
    for c in key:
        position = find_in_matrix(matrix, c)
        out.append([c] + list(position))
    return out
def conform_message(msg):
    msg = msg.lower().replace('j', 'i')
    regex = re.compile('[^a-z]')
    msg = regex.sub('', msg)
    prev = None
    msg_addx = ''
    for idx, char in enumerate(msg):
        if prev == char:
            if char == 'x':
                msg_addx += 'q'
            else:
                msg_addx += 'x'
        msg_addx += char
        prev = char
    if len(msg_addx) % 2:
        if msg_addx[-1] == 'x':
            msg_addx = msg_addx + 'q'
        else:
            msg_addx = msg_addx + 'x'
    print('Conformed message: {}'.format(msg_addx))

    # get digraphs
    return get_digraphs(msg_addx)
def get_digraphs(msg):
    out = []
    n = 2
    for i in range(0, len(msg), n):
        out.append(msg[i:i+n])
    return out


option = None
while True:
    print("Options")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

    option = input("Choose your option: ")
    if option == '1' or option == '2':
        break
    elif option == '3':
        sys.exit()
    else:
        print("Invalid option")

key = None
while True:
    key = input("Enter encoding key: ")
    if valid_key(key):
        break
    else:
        print("Invalid key, please enter an alphabetic lowercase string with no repeated characters and a minimum length of 2.\nIt also cannot contain the letter “j“.")
        key = None
print(" ")
if option == '1' and key is not None:
    matrix = create_matrix(key)
    message = input("Enter message to encrypt: ")
    digraphs = conform_message(message)
    encoded = ''
    for digraph in digraphs:
        p = find_digraph_in_matrix(matrix, digraph)
        # same row
        if p[0][1] == p[1][1]:
            col_0 = p[0][2] + 1
            if col_0 > 4:
                col_0 = 0
            col_1 = p[1][2] + 1
            if col_1 > 4:
                col_1 = 0
            encoded += matrix[p[0][1]][col_0]
            encoded += matrix[p[1][1]][col_1]
        # same column
        elif p[0][2] == p[1][2]:
            row_0 = p[0][1] + 1
            if row_0 > 4:
                row_0 = 0
            row_1 = p[1][1] + 1
            if row_1 > 4:
                row_1 = 0
            encoded += matrix[row_0][p[0][2]]
            encoded += matrix[row_1][p[1][2]]
        # if on different rows/columns, exchange columns
        else:
            encoded += matrix[p[0][1]][p[1][2]]
            encoded += matrix[p[1][1]][p[0][2]]
    print('Encrypted message: {}'.format(encoded))
    sys.exit()

elif option == '2' and key is not None:
    matrix = create_matrix(key)
    message = input("Enter message to decrypt: ")
    digraphs = get_digraphs(message)
    decoded = ''
    for digraph in digraphs:
        p = find_digraph_in_matrix(matrix, digraph)
        # same row
        if p[0][1] == p[1][1]:
            col_0 = p[0][2] - 1
            if col_0 < 0:
                col_0 = 4
            col_1 = p[1][2] - 1
            if col_1 < 0:
                col_1 = 4
            decoded += matrix[p[0][1]][col_0]
            decoded += matrix[p[1][1]][col_1]
        # same column
        elif p[0][2] == p[1][2]:
            row_0 = p[0][1] - 1
            if row_0 < 0:
                row_0 = 4
            row_1 = p[1][1] - 1
            if row_1 < 0:
                row_1 = 4
            decoded += matrix[row_0][p[0][2]]
            decoded += matrix[row_1][p[1][2]]
        # if on different rows/columns, exchange columns
        else:
            decoded += matrix[p[0][1]][p[1][2]]
            decoded += matrix[p[1][1]][p[0][2]]
    print('Decrypted message: {}'.format(decoded))
    sys.exit()

