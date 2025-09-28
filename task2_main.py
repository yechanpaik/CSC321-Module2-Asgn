def submit(input_string: str) -> bytes:
    prepended_string = "userid=456;userdata=" + input_string + ";session-id=31337"
    # url_encoded_string = prepended_string.replace("=", "%3D").replace(";", "%3B")
    url_encoded_string = quote(prepended_string, safe='') #replaces special characters with url encodings dynamically
    
    utf_encoded_string = url_encoded_string.encode('utf-8')
    
    print(f"utf: {utf_encoded_string}")
    padded_string_bytes: bytes = pad(utf_encoded_string, 16)

    plaintext_blocks = [padded_string_bytes[i:i+16] for i in range(0, len(padded_string_bytes), 16)]

    ciphertext = encrypt_with_cbc(key, iv, plaintext_blocks)
    return ciphertext
