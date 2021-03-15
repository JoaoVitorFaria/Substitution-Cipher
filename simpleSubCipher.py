#code based on the book Crackig Codes with Python

import pyperclip, sys, random
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    my_message =  "If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell"
    #my_key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'# it can set as my_key = getRandomKey()
    my_key=getRandomKey()
    my_mode = 'encrypt'#it can be set as 'decrypt'

    if not keyIsValid(my_key):
        sys.exit('There is an error in the key or symbol set.')
    if my_mode == 'encrypt':
        translated = encryptMessage(my_key, my_message)
    elif my_mode == 'decrypt':
        translated = decryptMessage(my_key, my_message)
    print('Using key %s'%(my_key))
    print('the %sed message is:' %(my_mode))
    print(translated)
    pyperclip.copy(translated)
    print()
    print("This message has been copied to the clipboard")

#the characthers from the key and the symbol set are copied to two lists.
#Then, it's used the sort method to guarantee that both are in the same numerical/alphabetical order.
#it allow us to compare both list to guarentee that there isn't a mistake
def keyIsValid(key):
    key_list = list(key)
    letters_list = list(LETTERS)
    key_list.sort()
    letters_list.sort()
    return key_list == letters_list

def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
    translated = ''
    chars_a = LETTERS
    chars_b = key
    #the decryption process looks up that letter's index in key and replaces
    #the character with the letter at the same index in the LETTERS parameter
    #That's why we may need to invert the characters order    
    if mode == 'decrypt':
        chars_a, chars_b = chars_b, chars_a
    #in the encryption process we don't need to invert the characters
    for symbol in message:
        if symbol.upper() in chars_a:
            sym_index = chars_a.find(symbol.upper())
            #the isupper is just to guarantee that i'm copying the letter
            #in uppercase if it's already is in uppercase at the orignal message
            if symbol.isupper():
                translated += chars_b[sym_index].upper()
            else:
                #guarantee that im copying the lowercase letters
                translated += chars_b[sym_index].lower()
        else:
            translated += symbol
    return translated

def getRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return ''.join(key)

if __name__ == '__main__':
    main()
