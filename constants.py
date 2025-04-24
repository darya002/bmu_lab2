# Градус полинома для поля Галуа (x^8 + x^4 + x^3 + x + 1)
m = 0x11b

def galois_mult(x, y):
    result = 0
    while y > 0:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x >= 0x100:
            x ^= m
    return result

def galois_inv(x):
    return galois_mult(x, 0x0e)

def affine_transformation(x):
    return ((x >> 4) ^ (x)) & 0xff

def generate_s_box():
    s_box = []
    for x in range(256):
        if x == 0:
            s_box.append(0)
        else:
            inv = galois_inv(x)
            s_box.append(affine_transformation(inv))
    return s_box

def print_s_box(s_box):
    print("S-box:")
    for i in range(0, 256, 16):
        row = " ".join([f"{s_box[j]:02x}" for j in range(i, i+16)])
        print(row)

s_box = generate_s_box()
print_s_box(s_box)

def generate_inv_s_box(s_box):
    inv_s_box = [0] * 256
    for i, value in enumerate(s_box):
        inv_s_box[value] = i
    return inv_s_box

def print_inv_s_box(inv_s_box):
    print("Inverse S-box:")
    for i in range(0, 256, 16):
        row = " ".join([f"{inv_s_box[j]:02x}" for j in range(i, i+16)])
        print(row)

inv_s_box = generate_inv_s_box(s_box)
print_inv_s_box(inv_s_box)

r_con = [
    0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80,
    0x1B, 0x36
]
