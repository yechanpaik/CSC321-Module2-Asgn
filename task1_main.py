from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

KEY_LEN_PLACEHOLDER = int(128/8)
#Task 1
#part 1: program takes in a plaintext file (.txt)
plaintext_blocks = []
filename = input("Enter the file name: ")
with open(filename, 'rb') as file:
    contents = file.read(16)
    while(contents):
        if(len(contents) < 16): 
            padding = bytes([16-len(contents)]) * (16-len(contents)) #pads with the value: number of padding required
            padded_plaintext = contents + padding
            plaintext_blocks.append(padded_plaintext)
        else:
            plaintext_blocks.append(contents)
        contents = file.read(16)

#break file down into plaintext[]: an array of strings 128bits each || Blocks
#   with padding as neccessary or at the end
   
print(f"parsed array of plaintext_blocks: \n{plaintext_blocks}\n")

# region BEGIN ECB
#part 2: generate a random key 
key = get_random_bytes(KEY_LEN_PLACEHOLDER)

#a Cipher is a sequence of operations that will convert plaintext into ciphertext, 
#   essentially handling the 'encryption' of the plaintext
#AES.new() generates a cipher
cipher_ecb = AES.new(key, AES.MODE_ECB)

#part 3: use the key to encrypt the plaintext file and make a new file

ciphertext_blocks_ecb = []
for blocks in plaintext_blocks:
    encrypted_block_ecb = cipher_ecb.encrypt(blocks)
    ciphertext_blocks_ecb.append(encrypted_block_ecb)
    
ciphertext_ecb = b''.join(ciphertext_blocks_ecb) #use the array to build a ciphertext string

print(f"final ciphertext_ecb: \n{ciphertext_ecb}\n")
# endregion ECB

# --- BEGIN CBC 
cipher_cbc = AES.new(key, AES.MODE_CBC)

ciphertext_blocks_cbc = []
for blocks in plaintext_blocks:
    encrypted_block_cbc = cipher_cbc.encrypt(blocks)
    ciphertext_blocks_cbc.append(encrypted_block_cbc)

ciphertext_cbc = b''.join(ciphertext_blocks_cbc)
    

print(f"final ciphertext_cbc: \n{ciphertext_cbc}\n")

#cbc_iv = get_random_bytes(KEY_LEN_PLACEHOLDER)
#i = 0
# for blocks in plaintext_blocks:
#   if(i==0):
#       one_before = blocks
#       encrypted_block_cbc = cipher_cbc.encrypt(blocks XOR iv)
#       i = 1
#   else:
#       encrypted_block_cbc  = cipher_cbc.encrypt(blocks XOR one_before)
#       one_before = blocks
#   ciphertext_blocks_cbc.append(encrypted_block_cbc)

#ciphertext_cbc = b''.join(ciphertext_blocks_cbc)

#print(f"final ciphertext_cbc: \n{ciphertext_cbc}\n")
# --- END CBC


# final ciphertext_ecb:
# b'\x93Ze\x1cQ6\x93}\x13BB\x9d\x85\x88Zu\x80,z\xcf\x95\x04&i\xb3t\x95\x1c\xe2\xeb\xff\x95\x8b\xb3\xdd\x8bd\xfa\x83\xfd)\xdccC\x08\xaboX\xe5\xcd\xb5\x9cY\x11\xd8\x16\x88\xf8h\xaf\xda\xee\x9a\x8fv\x05\xc3\xf4\xe8\xbf\xa5\x9bJR\xca\xd8\x8f\xa8\xea\xc6j\xeb`\x90\xf0\x82\x7f*)\xed\xc2\x19Y\xaa|C'

# final ciphertext_cbc: 
# b'\x978\x0f;\xa2%\xfd\x1dC\xab\xa4\x9fp\xe1\\x\x1e\xeduoQ\x06,\xf9\x96\x97\x9e9\xa5\xab\xcd\xc1\x15$\xcf\x82f\x82C\x80f\xdbK\x88U\xd8\xd4\x04\xb8\xa4\x170\xaeRS\x83nh\x81\xfb\xfb\xcc\x0f\xc5\x00\x83\x07,\xd8\x82\x08\xa0\xfb\tC\x89\xc8W\xe04\xe7\x96\xebN\xee\x81O\xb7f\x8c\xb8\xccoO\x11\xf4'



# --- Task 2

# --- BEGIN SUBMIT()
original_string = input("Enter a string: ")

prepended_string = "userid=456; userdata=" + original_string

appended_string = prepended_string + ";session-id=31337"

url_encoded_string_first_half = appended_string.replace("=", "%3D")
url_encoded_string = url_encoded_string_first_half.replace(";", "%3B")

padded_string = pad(url_encoded_string.encode('utf-8'), 16)