from constants import *

def sub_word(word):
    return [s_box[b] for b in word]

def rot_word(word):
    return word[1:] + word[:1]

def key_expansion(key):
    key_symbols = [b for b in key]
    if len(key_symbols) != 16:
        raise ValueError("Key must be 16 bytes long for AES-128")

    # Первые 4 слова = исходный ключ
    w = [key_symbols[i:i + 4] for i in range(0, 16, 4)]

    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= r_con[i // 4 - 1]
        word = [w[i - 4][j] ^ temp[j] for j in range(4)]
        w.append(word)

    return w

def print_round_keys(expanded_key):
    print("Раундовые ключи:")
    for i in range(11):  # 11 ключей для 10 раундов + начальный
        key = expanded_key[i*4:(i+1)*4]
        flat = sum(key, [])
        print(f"Round {i:2}: {' '.join(f'{b:02x}' for b in flat)}")

# Пример: 16-байтный ключ
key = b'ThisIsASecretKey'
expanded = key_expansion(key)
print_round_keys(expanded)

