from aes_encription import *

def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = inv_s_box[state[i][j]]
    return state

def inv_shift_rows(state):
    for i in range(1, 4):
        state[i] = state[i][-i:] + state[i][:-i]
    return state

def mul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set:
            a ^= 0x1B
        b >>= 1
    return p

def inv_mix_single_column(col):
    c0 = mul(col[0], 0x0e) ^ mul(col[1], 0x0b) ^ mul(col[2], 0x0d) ^ mul(col[3], 0x09)
    c1 = mul(col[0], 0x09) ^ mul(col[1], 0x0e) ^ mul(col[2], 0x0b) ^ mul(col[3], 0x0d)
    c2 = mul(col[0], 0x0d) ^ mul(col[1], 0x09) ^ mul(col[2], 0x0e) ^ mul(col[3], 0x0b)
    c3 = mul(col[0], 0x0b) ^ mul(col[1], 0x0d) ^ mul(col[2], 0x09) ^ mul(col[3], 0x0e)
    return [c0, c1, c2, c3]

def inv_mix_columns(state):
    for i in range(4):
        col = [state[j][i] for j in range(4)]
        mixed = inv_mix_single_column(col)
        for j in range(4):
            state[j][i] = mixed[j]
    return state

def decrypt_block(block, expanded_key):
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = block[i]

    round_keys = [expanded_key[i*4:(i+1)*4] for i in range(11)]

    state = add_round_key(state, round_keys[10])
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)

    for rnd in range(9, 0, -1):
        state = add_round_key(state, round_keys[rnd])
        state = inv_mix_columns(state)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)

    state = add_round_key(state, round_keys[0])

    output = []
    for i in range(4):
        for j in range(4):
            output.append(state[j][i])
    return bytes(output)

decrypted = decrypt_block(ciphertext, expanded)
print("Расшифрованный блок:")
print(decrypted)
