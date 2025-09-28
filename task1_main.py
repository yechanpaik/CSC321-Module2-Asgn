from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor

KEY_LEN_PLACEHOLDER = int(128/8)
#Task 1
#part 1: program takes in a plaintext file (.txt)
plaintext_blocks = []
filename = input("Enter the bmp name: ")
header: bytearray = None
with open(filename, 'rb') as file:
    header = file.read(54)
    # header
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
ciphertext_ecb = b''.join()

print(f"final ciphertext_ecb: \n{ciphertext_ecb}\n")
#build a new file with the ciphertext
with open("encrypted_ecb_" + filename, 'wb') as file:
    file.write(header)
    file.write(ciphertext_ecb)
    
# endregion ECB

# region BEGIN CBC 
cipher_cbc = AES.new(key, AES.MODE_CBC)

ciphertext_blocks_cbc = []
# for blocks in plaintext_blocks:
#     encrypted_block_cbc = cipher_cbc.encrypt(blocks)
#     ciphertext_blocks_cbc.append(encrypted_block_cbc)

# ciphertext_cbc = b''.join(ciphertext_blocks_cbc)
    
cbc_iv = get_random_bytes(KEY_LEN_PLACEHOLDER)
i = 0
for blocks in plaintext_blocks:
  if(i==0):
      one_before = blocks
      encrypted_block_cbc = cipher_cbc.encrypt(strxor(blocks, cbc_iv))
      i = 1
  else:
      encrypted_block_cbc  = cipher_cbc.encrypt(strxor(blocks, one_before))
      one_before = blocks
  ciphertext_blocks_cbc.append(encrypted_block_cbc)

ciphertext_cbc = b''.join(ciphertext_blocks_cbc)

print(f"final ciphertext_cbc: \n{ciphertext_cbc}\n")
#build a new file with the ciphertext
with open("encrypted_cbc_" + filename, 'wb') as file:
    file.write(header)
    file.write(ciphertext_ecb)
    
# endregion END CBC