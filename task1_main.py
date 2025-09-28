from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor

KEY_LEN_PLACEHOLDER = int(128/8)

def encrypt_with_ecb(key: bytes, plaintext_blocks: list[bytes]):
    #key: a 128bit random byte that acts as the key
    #plaintext_blocks: an array of plaintext 16 bytes ea
    #RETURNS complete ciphertext
    
    #Cipher: a sequence of operations that will convert plaintext into ciphertext, 
    #   essentially handling the 'encryption' of the plaintext
    cipher_ecb = AES.new(key, AES.MODE_ECB) # AES.new() generates a cipher

    ciphertext_blocks_ecb = []
    for blocks in plaintext_blocks:
        encrypted_block_ecb = cipher_ecb.encrypt(blocks)
        ciphertext_blocks_ecb.append(encrypted_block_ecb)
        
    ciphertext_ecb = b''.join(ciphertext_blocks_ecb) #use the array to build a ciphertext string

    print(f"Encrypted ciphertext (ECB): \n{ciphertext_ecb}\n")
    return ciphertext_ecb
    
def encrypt_with_cbc(key, iv: bytes, plaintext_blocks: list[bytes]): 
    #key: a 128bit random byte that acts as the key
    #plaintext_blocks: an array of plaintext 16 bytes ea
    #RETURNS complete ciphertext
    
    cipher_cbc = AES.new(key, AES.MODE_ECB)

    ciphertext_blocks_cbc = []
     
    #Process for cbc encryption:
    # First block:
        # XOR the first plaintext block with the IV.
        # Encrypt the result to get the first ciphertext block.
    # Subsequent blocks:
        # XOR the plaintext block with the previous ciphertext block.
        # Encrypt the result with a cipher to get the next ciphertext block.
        
    #!Note: Cipher can be ECB or CBC it doesn't matter since its only for one block
    #What makes it CBC Encryption is the XOR masks between each block encryption
    # see discord pic 
    
    i = 0
    for blocks in plaintext_blocks:
        if (i==0):
            encrypted_block_cbc = cipher_cbc.encrypt(strxor(blocks, iv))
            prev_block = encrypted_block_cbc
            i = 1
        else:
            encrypted_block_cbc  = cipher_cbc.encrypt(strxor(blocks, prev_block))
            prev_block = encrypted_block_cbc
        ciphertext_blocks_cbc.append(encrypted_block_cbc)

    ciphertext_cbc = b''.join(ciphertext_blocks_cbc)

    print(f"Encrypted ciphertext (CBC): \n{ciphertext_cbc}\n")
    return ciphertext_cbc

def main():
    #Task 1
    #part 1: program takes in a plaintext file (.txt)
    plaintext_blocks = []
    filename = input("Enter the bmp name: ")
    header: bytearray = None

    #break plaintext down into plaintext[]: an array of strings 128bits each
    #with padding as neccessary or at the end

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

    print(f"parsed array of plaintext_blocks: \n{plaintext_blocks}\n")

    key = get_random_bytes(KEY_LEN_PLACEHOLDER)
    ciphertext_ecb = encrypt_with_ecb(key, plaintext_blocks)
    with open("encrypted_ecb_" + filename, 'wb') as file:
        file.write(header)
        file.write(ciphertext_ecb)
        
    cbc_iv = get_random_bytes(KEY_LEN_PLACEHOLDER)
    ciphertext_cbc = encrypt_with_cbc(key, cbc_iv, plaintext_blocks)
    with open("encrypted_cbc_" + filename, 'wb') as file:
        file.write(header)
        file.write(ciphertext_cbc)
        
if __name__ == "__main__":
    main()
        