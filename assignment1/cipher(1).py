def break_cipher(e,a,t):
    key = e - a
    result = ''
    for character in t:
        result += chr(ord("A") + (ord(character) - ord("A") + key) % 26)
    return result

encrypted = ord(input("Please enter the sample encrypted string:")[0:1])
actual = ord(input("Please enter the corresponding decrypted string:")[0:1])
tobedecrypted = input("Please enter the string you want to decrypt:")
result = break_cipher(encrypted, actual, tobedecrypted)
print(result)