from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from task1_main import encrypt_with_cbc, encrypt_with_ecb
from urllib.parse import quote, unquote

KEY_LEN_PLACEHOLDER = int(128/8)

key = get_random_bytes(KEY_LEN_PLACEHOLDER)  
iv = get_random_bytes(KEY_LEN_PLACEHOLDER)

def decrypt_with_cbc(iv: bytes, ciphertext: bytes) -> str:
    #function not modular because it unpads and decode utf-8
    cipher_cpc = AES.new(key, AES.MODE_ECB)
    
    cipherblocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)] 
    plaintext_blocks = []
    
    #Process for CBC decryption:
    #   for decrypting ciphertext block Cn:
    #       X = cipher.decrypt(Cn) // X is a placeholder
    #       Let plaintext block Pn = X xor <previous ciphertext block>
    #!Note that after decryption, X is xor with the previous "ciphertext" block
    # and not the previous decrypted/plaintext block   
    
    previous_block = iv
    for blocks in cipherblocks:
        decrypted_block = cipher_cpc.decrypt(blocks)
        plaintext_block = strxor(decrypted_block, previous_block)
        previous_block = blocks
        
        plaintext_blocks.append(plaintext_block)
    
    plaintext = b''.join(plaintext_blocks)
    plaintext = unpad(plaintext, 16).decode('utf-8') 
       
    return plaintext
    
def submit(input_string: str) -> bytes:
    prepended_string = "userid=456;userdata=" + input_string + ";session-id=31337"
    # url_encoded_string = prepended_string.replace("=", "%3D").replace(";", "%3B")
    url_encoded_string = quote(prepended_string, safe='') #replaces special characters with url encodings dynamically
    
    utf_encoded_string = url_encoded_string.encode('utf-8')
    
    print(f"utf: {utf_encoded_string}\n")
    padded_string_bytes: bytes = pad(utf_encoded_string, 16)

    plaintext_blocks = [padded_string_bytes[i:i+16] for i in range(0, len(padded_string_bytes), 16)]

    ciphertext = encrypt_with_cbc(key, iv, plaintext_blocks)
    return ciphertext

def verify(iv_key: bytes, ciphertext: bytes) -> bool:
    cbc_decryption = decrypt_with_cbc(iv_key, ciphertext)

    plaintext_unquoted = unquote(cbc_decryption)
    plaintext = plaintext_unquoted[20:-17]
    print(f"Decrypted plaintext (CBC): \n{plaintext}\n")


    if(";admin=true;" in cbc_decryption):
        print("True")
        return True
    else:
        print("False")
        return False

def main():
    input_string = input("Enter a string: ")
    
    enc = submit(input_string)
    
    # dec = cipher.decrypt(enc)
    dec = verify(iv, enc)
    

if __name__ == "__main__":
    main()