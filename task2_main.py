# --- Task 2

# region BEGIN SUBMIT()
original_string = input("Enter a string: ")

prepended_string = "userid=456; userdata=" + original_string

appended_string = prepended_string + ";session-id=31337"

url_encoded_string_first_half = appended_string.replace("=", "%3D")
url_encoded_string = url_encoded_string_first_half.replace(";", "%3B")

padded_string = pad(url_encoded_string.encode('utf-8'), 16)

# endregion SUBMIT()

#region BEGIN VERIFY()

#endregion VERIFY()