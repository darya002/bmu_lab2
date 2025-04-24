from key_expansion import *

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = s_box[state[i][j]]
    return state

def shift_rows(state):
    for i in range(1, 4):
        state[i] = state[i][i:] + state[i][:i]
    return state

def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1)

def mix_single_column(col):
    t = col[0] ^ col[1] ^ col[2] ^ col[3]
    u = col[0]
    col[0] ^= t ^ xtime(col[0] ^ col[1])
    col[1] ^= t ^ xtime(col[1] ^ col[2])
    col[2] ^= t ^ xtime(col[2] ^ col[3])
    col[3] ^= t ^ xtime(col[3] ^ u)
    return col

def mix_columns(state):
    for i in range(4):
        col = [state[j][i] for j in range(4)]
        mixed = mix_single_column(col)
        for j in range(4):
            state[j][i] = mixed[j]
    return state

def add_round_key(state, round_key):
    for i in range(4):  # строки
        for j in range(4):  # столбцы
            state[i][j] ^= round_key[j][i]
    return state

def encrypt_block(block, expanded_key):
    state = [[0]*4 for _ in range(4)]

    for i in range(16):
        state[i % 4][i // 4] = block[i]

    round_keys = [expanded_key[i*4:(i+1)*4] for i in range(11)]
    state = add_round_key(state, round_keys[0])

    for rnd in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[rnd])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])

    output = []
    for i in range(4):
        for j in range(4):
            output.append(state[j][i])
    return bytes(output)


plaintext = b'Top secret info!'
key = b'And this is  key'

expanded = key_expansion(key)
ciphertext = encrypt_block(plaintext, expanded)

print("Зашифрованный блок:")
print(ciphertext.hex())
