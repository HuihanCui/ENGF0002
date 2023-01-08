import enchant

list = enchant.Dict("en_GB")

def break_cipher(text):
    for key in range(1,27):
        result = ''
        for character in text:
            result += chr(ord("A") + (ord(character) - ord("A") + key) % 26)
        if list.check(result):
            print("the decrypted string is " + result)
            
        

break_cipher("RJXXFLJ")
