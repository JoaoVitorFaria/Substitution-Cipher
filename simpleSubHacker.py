#code based on the book Cracking Codes with Python
import os, re, copy, pyperclip, simpleSubCipher, wordPatterns, makeWordPatterns


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    print("hacking...")
    letter_mapping = hackSimpleSub(message)

    print("Mapping:")
    print(letter_mapping)
    print()
    print('Original Ciphertext:')
    print(message)
    print()
    print("Copying hacked message to clipboard:")
    hacked_message = decryptWithCipherLetterMapping(message, letter_mapping)
    pyperclip.copy(hacked_message)
    print(hacked_message)

#this function set up a new dictionary that is a blank cipherlettter mapping
def getBlankCipherLetterMapping():
    return  {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 
 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 
 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 
 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

#this function maps every letter in candidate to the cipherletter at the corresponding index position in the cipherword
#and then adds that letter to latter_mapping if it isn't already there.
def addLettersToMapping(letter_mapping, cipherword, candidate):
    for i in range (len(cipherword)):
        if candidate[i] not in letter_mapping[cipherword[i]]:
            letter_mapping[cipherword[i]].append(candidate[i])

#this function takes two cipherletter mappings, passed as map_a and map_b, and return a merged mapping
#it add potencial decryption letter to a new blank map only if it exist in both maps
def intersectMappings(map_a, map_b):
    intersected_mapping = getBlankCipherLetterMapping()
    for letter in LETTERS:
        #if i don't have any potencial decryption letter in my map_a, then i just have to copy all the letter from map_b
        if map_a[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_b[letter])
        elif map_b[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_a[letter])
        else:
            for mapped_letter in map_a[letter]:
                if mapped_letter in map_b[letter]:
                    intersected_mapping[letter].append(mapped_letter)
    return intersected_mapping

#this function searches for any cipherletters in the letter_mapping that have only one potencial decryption letter, and, then,
#removes the newsly solved letter from the entire cipherletter mapping
def removeSolvedLettersFromMapping(letter_mapping):
    loop_again= True
    while loop_again:
        loop_again= False

        solved_letters=[]
        for cipher_letter in LETTERS:
            if len(letter_mapping[cipher_letter])==1:
                solved_letters.append(letter_mapping[cipher_letter][0])

        for cipher_letter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipher_letter])!= 1 and s in letter_mapping[cipher_letter]:
                    letter_mapping[cipher_letter].remove(s)
                    if len(letter_mapping[cipher_letter]) == 1:
                        loop_again = True
    return letter_mapping

def hackSimpleSub(message):
    intersected_map = getBlankCipherLetterMapping()
    #here the code looks through the uppercase message variable and remove tha characters defined in nonLettersOrSpacePattern.
    #those characters  are replaced by ''
    cipher_word_list = nonLettersOrSpacePattern.sub('',message.upper()).split()
    for cipher_word in cipher_word_list:
        candidate_map = getBlankCipherLetterMapping()
        word_pattern = makeWordPatterns.getWordPattern(cipher_word)
        #if the word_pattern doesn't exist in the key of the wordPatterens.all patterns dictionary, the cipherword doesn't
        #exist in the dictionary file and won't get a mapping.
        if word_pattern not in wordPatterns.allPatterns:
            continue
        #here the code interacts though a list of words that match with this pattern
        for candidate in wordPatterns.allPatterns[word_pattern]:
            addLettersToMapping(candidate_map, cipher_word, candidate)

        intersected_map = intersectMappings(intersected_map, candidate_map)

    return removeSolvedLettersFromMapping(intersected_map)

def decryptWithCipherLetterMapping(cipher_text, letter_mapping):
    #return a string of the ciphertext decrypted with the letter mapping
    key = ['x']*len(LETTERS)
    for cipher_letter in LETTERS:
        if len(letter_mapping[cipher_letter])==1:
            key_index = LETTERS.find(letter_mapping[cipher_letter][0])
            #it's the index of the decryption letter in LETTERS
            key[key_index] = cipher_letter
        else :
            #if there isn't a solution, teh function inserts an underscore for that cipherletter.
            cipher_text = cipher_text.replace(cipher_letter.lower(), '_')
            cipher_text = cipher_text.replace(cipher_letter.upper(), '_')
    key = ''.join(key)
    #finally, the string is passed to the decrytpMessage function in the simbpleSubCipher program.
    return simpleSubCipher.decryptMessage(key,cipher_text)

if __name__ =='__main__':
    main()



            
