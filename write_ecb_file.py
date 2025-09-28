# Write the BMP header followed by the ECB ciphertext
def write_ecb_encrypted_file(header, ciphertext, out_filename):
    with open(out_filename, 'wb') as f:
        f.write(header)
        f.write(ciphertext)

# Usage example:
write_ecb_encrypted_file(header, ciphertext_ecb, 'ecb_encrypted.bmp')
