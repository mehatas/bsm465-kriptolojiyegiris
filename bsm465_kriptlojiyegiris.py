import random

# anahtarı expansion tablosu yardımıyla genişlet ve metinle xor'lama işlemlerini gerçekleştir
def expand_and_xor(text, round_key):
    expansion_table = [
        56, 53, 54, 55,
        1,  2,  3,  4,
        5,  6,  7,  8,
        9,  10, 11, 12,
        13, 14, 15, 16,
        17, 18, 19, 20,
        21, 22, 23, 24,
        25, 26, 27, 28,
        29, 30, 31, 32,
        33, 34, 35, 36,
        37, 38, 39, 40,
        41, 42, 43, 44,
        45, 46, 47, 48,
        49, 50, 51, 52,
        53, 54, 55, 56,
        2, 3, 4, 1
    ]
    expanded_key = ''.join(round_key[i - 1] for i in expansion_table)
    xor_result = ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(expanded_key, text))
    return xor_result

# string olarak girilen girdilerimizin binary formatına dönüştüren fonksiyon
def string_to_binary(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text
# binary formatında olan verileri stringe çeviren fonksiyon
def binary_to_string(binary_text):
    text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    return text
# verilen metni bloklara bölmemize sağlayacak olan fonksiyon
def split_blocks(binary_text, block_size):
    blocks = [binary_text[i:i+block_size] for i in range(0, len(binary_text), block_size)]
    return blocks

def initial_permutation(block):
    permutation_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    permuted_block = ''.join(block[i - 1] for i in permutation_table)
    return permuted_block
# final permütasyonu
def final_permutation(block):
    final_permutation_table = [
      40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25
    ]
    permuted_block = ''.join(block[i - 1] for i in final_permutation_table)
    return permuted_block
# başlangıç permütasyonu
def key_initial_permutation(key):
    permutation_table = [
        125, 22, 101, 63, 62, 38, 95, 93,
        97, 92, 34, 18, 67, 107, 73, 10,
        36, 77, 102, 82, 2, 99, 81, 31,
        45, 42, 53, 100, 119, 89, 108, 11,
        66, 47, 15, 19, 115, 68, 13, 41,
        52, 57, 54, 17, 61, 111, 20, 127,
        39, 87, 1, 122, 35, 78, 121, 9,
        12, 84, 109, 44, 103, 50, 106, 43,
        110, 79, 58, 59, 65, 74, 7, 29,
        118, 86, 55, 83, 26, 114, 33, 25,
        117, 123, 30, 76, 113, 85, 94, 90,
        14, 5, 46, 126, 4, 71, 23, 27,
        116, 37, 70, 60, 3, 98, 28, 91,
        105, 21, 75, 51, 69, 124, 49, 6
    ]
    permuted_key = ''.join(key[i - 1] for i in permutation_table)
    return permuted_key
# Anahtar üretim aşamalarını içeren fonksiyon
def generate_key(key_):
    key = key_
    # anahtarı karıştır ve parite bitlerini çıkart
    permuted_key = key_initial_permutation(key)
    # Karışmış 112 biti iki kısma ayır
    left, right = permuted_key[:56], permuted_key[56:]
    # 16 tur boyunca kaydırma işlemlerini uygula ve döngü anahtarlarını üret
    for round_num in range(1, 17):
        # 1. ve 2. 9. 16. turda 2 bit sola, diğer turlarda 4 bit sola kaydır
        shift_amount = 2 if round_num in [1, 2, 9, 16] else 4
        left = left[shift_amount:] + left[:shift_amount]
        right = right[shift_amount:] + right[:shift_amount]
        # Döngüde kullanılacak anahtarı oluştur.
        round_key = left + right
        # Döngü anahtarını döndür
        yield round_key
# Metindeki eksik bitleri tamamlamak için padding işlemini gerçekleştiren fonksiyon
def pad_text(text, block_size):
    padding_length = block_size - (len(text) % block_size)
    padded_text = text + chr(padding_length) * padding_length
    return padded_text

# Şifreleme işlemleri
def encrypt_block(block, key):
    # Bloğu iki kısma ayır
    left, right = block[:64], block[64:]

    # Bloklara başlangıç permütasyonlarını uygula
    left = initial_permutation(left)
    right = initial_permutation(right)

    # Anahtar üretimi ve şifreleme işlemleri
    for round_key in generate_key(key):
        # Anahtar genişletme ve XOR işlemleri
        round_key_left, round_key_right = round_key[:56], round_key[56:]
        expanded_left_xor = expand_and_xor(left, round_key_right)
        expanded_right_xor = expand_and_xor(right, round_key_left)

        # Sağ ve sol kısımları güncelle
        left, right = expanded_right_xor, expanded_left_xor

    # Bloklara final permütasyonlarını uygula
    left = final_permutation(left)
    right = final_permutation(right)

    ciphertext = right + left

    return ciphertext

# Kullanıcıdan şifrelemek için metin alıyoruz
plaintext = input("Şifrelenecek metni girin: ")

# Alınan metni şifrelemek için kullanılıcak anahatarı kullanıcıdan alıyoruz
_key = input("anahtar metni girin:16 karakter ")

# Alınan anahtarı binary formatına çeviriyoruz
_key = string_to_binary(_key)

# Metni belirli bir blok boyutuna kadar dolduruyoruz(bloklarda 128 bitten eksik veri olursa doldurma işlemi yapılıyor)
padded_text = pad_text(plaintext, 16)

# Şifrelenecek metni binary formatına çeviriyoruz
binary_text = string_to_binary(padded_text)

# Metni 128 bitlik bloklara ayıyoruz
blocks = split_blocks(binary_text, 128)

all_ciphertext = ""
for i, block in enumerate(blocks):
    ciphertext_block = encrypt_block(block,_key)  # Şifreleme işlemi gerçekleştiriliyor
    all_ciphertext += ciphertext_block

# Şifrelenmiş metni string formatında ekrana yazdır
ciphertext_string = binary_to_string(all_ciphertext)
print(f"Şifrelenmiş Metin: {ciphertext_string}")