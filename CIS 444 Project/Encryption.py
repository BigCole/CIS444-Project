import time

#DES:

# NOTE: hexToBin() and binToHex() functions created with inspiration from other sources
# Input: Ciphertext(hexadeciaml) from .csv -> converted to binary to be used with DES
# Output: plaintext(ASCII) from hex(binary(DES ouput))
#
keys = []
plaintext = ""


def shiftLeft(chunk, numShift):
    shifted = ""
    for i in range (numShift):
        for j in range(1, len(chunk)):
            shifted += chunk[j]
        shifted += chunk[0]
        chunk = shifted
        shifted = ""
    return chunk

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans

def hexToBin(hex):
    mp = {'0' : "0000", 
          '1' : "0001",
          '2' : "0010", 
          '3' : "0011",
          '4' : "0100",
          '5' : "0101", 
          '6' : "0110",
          '7' : "0111", 
          '8' : "1000",
          '9' : "1001", 
          'A' : "1010",
          'B' : "1011", 
          'C' : "1100",
          'D' : "1101", 
          'E' : "1110",
          'F' : "1111" }
    bin = ""
    for i in range(len(hex)):
        bin = bin + mp[hex[i]]
    return bin

def decToBin(num):
    res = bin(num).replace("0b", "")
    if(len(res)%4 != 0):
        div = len(res) / 4
        div = int(div)
        counter =(4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

def binToDec(binary):
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal


def binToHex(bin):
    mp = {"0000" : '0', 
          "0001" : '1',
          "0010" : '2', 
          "0011" : '3',
          "0100" : '4',
          "0101" : '5', 
          "0110" : '6',
          "0111" : '7', 
          "1000" : '8',
          "1001" : '9', 
          "1010" : 'A',
          "1011" : 'B', 
          "1100" : 'C',
          "1101" : 'D', 
          "1110" : 'E',
          "1111" : 'F' }
    hex = ""
    for i in range(0,len(bin),4):
        ch = ""
        ch = ch + bin[i]
        ch = ch + bin[i + 1] 
        ch = ch + bin[i + 2] 
        ch = ch + bin[i + 3] 
        hex = hex + mp[ch]
          
    return hex

def generateKeys(key):
    global keys
    perm1 = [
    57,49,41,33,25,17,9, 
	1,58,50,42,34,26,18, 
	10,2,59,51,43,35,27, 
	19,11,3,60,52,44,36,		 
	63,55,47,39,31,23,15, 
	7,62,54,46,38,30,22, 
	14,6,61,53,45,37,29, 
	21,13,5,28,20,12,4
    ]

    perm2 = [ 
	14,17,11,24,1,5, 
	3,28,15,6,21,10, 
	23,19,12,4,26,8, 
	16,7,27,20,13,2, 
	41,52,31,37,47,55, 
	30,40,51,45,33,48, 
	44,49,39,56,34,53, 
	46,42,50,36,29,32 
	]

    permKey = ""
    for i in range(56):
        permKey += key[perm1[i] - 1]
    #print(permKey)

    leftKey = permKey[:28]
    rightKey = permKey[28:56]

    for i in range(16):
        if (i==0 or i==1 or i==8 or i==15):
            leftKey = shiftLeft(leftKey, 1)
            rightKey = shiftLeft(rightKey, 1)
        else:
            leftKey = shiftLeft(leftKey, 2)
            rightKey = shiftLeft(rightKey, 2)
    
        newKey = leftKey + rightKey
        roundKey = ""

        for i in range(48):
            roundKey += newKey[perm2[i] - 1]
        
        keys.append(roundKey)

def DES():
    global plaintext
    global keys

    initial_perm = [
	58,50,42,34,26,18,10,2, 
	60,52,44,36,28,20,12,4, 
	62,54,46,38,30,22,14,6, 
	64,56,48,40,32,24,16,8, 
	57,49,41,33,25,17,9,1, 
	59,51,43,35,27,19,11,3, 
	61,53,45,37,29,21,13,5, 
	63,55,47,39,31,23,15,7 
    ]

    expansion_table = [
	32,1,2,3,4,5,4,5, 
	6,7,8,9,8,9,10,11, 
	12,13,12,13,14,15,16,17, 
	16,17,18,19,20,21,20,21, 
	22,23,24,25,24,25,26,27, 
	28,29,28,29,30,31,32,1 
	] 

    substitution_boxes = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
			
		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
			[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
			[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],
	
		[ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
			[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
		
		[ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
			[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],
		
		[ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
			[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
		
		[ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
			[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
			[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],
		
		[ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
			[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
			[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],
		
		[ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
			[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
			[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
			[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]
    
    perm_table = [
	16,7,20,21,29,12,28,17, 
	1,15,23,26,5,18,31,10, 
	2,8,24,14,32,27,3,9,
	19,13,30,6,22,11,4,25
	] 

    inverse_perm = [
	40,8,48,16,56,24,64,32, 
	39,7,47,15,55,23,63,31, 
	38,6,46,14,54,22,62,30, 
	37,5,45,13,53,21,61,29, 
	36,4,44,12,52,20,60,28, 
	35,3,43,11,51,19,59,27, 
	34,2,42,10,50,18,58,26, 
	33,1,41,9,49,17,57,25 
    ]

    perm = ""
    for i in range(64):
        perm += plaintext[initial_perm[i] - 1]
    
    left = perm[0:32]
    right = perm[32:64]

    for i in range(0, 16):
        right_expanded = ""
        for j in range(48):
            right_expanded += right[expansion_table[j]-1]
    
        xored = xor(right_expanded, keys[i])
        res = ""
        for j in range(0, 8): 
            row = binToDec(int(xored[j*6] + xored[j*6 + 5]))
            col = binToDec(int(xored[j*6 + 1] + xored[j*6 + 2] + xored[j*6 + 3] + xored[j*6 + 4]))

            val = substitution_boxes[j][row][col]
            res += decToBin(val)
        
        perm2 = ""
        for j in range(0, 32):
            perm2 += res[perm_table[j] - 1]
        
        xored = xor(perm2, left)
        left = xored
        if(i < 15):
            temp = right
            right = xored
            left = temp
    
    combined_text = left + right
    ciphertext = ""

    for i in range(64):
        ciphertext += combined_text[inverse_perm[i] - 1]

    return ciphertext

def decrypt(cipher, hexKey):
    global plaintext
    global keys

    keys = []

    plaintext = hexToBin(cipher)
    generateKeys(hexToBin(hexKey))

    i = 15
    j = 0
    while(i > j):
        temp = keys[i]
        keys[i] = keys[j]
        keys[j] = temp
        i -= 1
        j += 1
    
    decrypted = DES()
    return decrypted
    
#Caesar Cipher:

def CS_Decrypt(ciphertext, key):

    #Store the original message:
    original_message = ""
    
    #for each char in ciphertext:
    for c in ciphertext:
        #if it's lower:
        if c.islower(): 
            #get current index of the current char (c):
            c_index = ord(c) - ord('a') 
            #change position of char based on key
            c_og_pos = (c_index - key) % 26 + ord('a')
            #set the original char to this new index:
            c_og = chr(c_og_pos)
            #add the char to the original message array:
            original_message += c_og
        else:#if not, add original to the message:
            original_message += c
            
    #Return the original message after decrypting:
    return original_message
    
def processCS(stringtodecrypt, dictionary):
    #arrays for average key times, decrypted messages, and accurate keyword:
    t_decrypt = []
    t_dict = []
    decrypted = [None] * 26
    matches = []
    
    #For range 0 to 26:
    for i in range(0,26):
        #Get current time before key is processed:
        tic = time.perf_counter()
        plain_text = CS_Decrypt(stringtodecrypt.lower(), i)
        toc = time.perf_counter()
        t_decrypt.append(toc - tic)
        
        
        tic = time.perf_counter()
        # Search through each word of the dictionary:
        for words in dictionary:
            if words == plain_text:
                matches.append([plain_text,i])   #change accurate if same word 
        #Get the time now using toc:
        toc = time.perf_counter()
        t_dict.append(toc - tic)

        #print("Decrypted",stringtodecrypt,"using key",i,"which resulted in",plain_text)
        
    #Return array of our matches [[matches],sum of time taken to decrypt, sum of time taken to check dictionary]
    return [matches,sum(t_decrypt),sum(t_dict)] 
    
def processDES(ciphertext, dictionary, finalkeyset):
    #Declare avg time to calculate DES as an array:
    match = None  
    matchkey = None
    
    #Get current time before key is processed:
    tic = time.perf_counter()
    
    for key in finalKeySet:
        try:
            result = decrypt(ciphertext, key.upper())
            decryptedHex = binToHex(result)
            text = bytearray.fromhex(decryptedHex).decode().rstrip('\x00')
            for words in dictionary:
                if words == text:
                    return [text, key, time.perf_counter() - tic]
                    break
        except:
            continue

#Begin main:

print("================================================================================\n")
#Get our command list (list of inputs):
commands = open("input.txt", "r", encoding='utf-8')
commandList = commands.read().split("\n")

#Get our dictionary as a list:
d = open("dictionary.txt", "r", encoding='utf-8')
dictionary = d.read().split("\n")

#Print out what we loaded in:
print("Loaded",len(dictionary),"words into the dictionary.")
d.close()
print("Found", len(commandList), "intercepted messages to process.\n")
commands.close()

output = []
outputtime = []

print("================================================================================")

print("\nGenerating Final Keyset...\n")

yearKey = []
for i in range(1935, 1950):
    result = ""
    year = hex(i)[2:]
    for j in range(5):
        result += year
    yearKey.append(result.upper())
        
finalKeySet = []
alphabet = ['A']

for letter in alphabet:
    for key in yearKey:
        newKey = ''.join(key + letter)
        finalKeySet.append(newKey.upper())
   
for key in finalKeySet:
    print(key)
    
print("\n================================================================================")

#Start processing commands:
for cmd in commandList:
    info = cmd.split(", ") #split the string up:
    print("Intercepted message [",info[3],"] from", info[2], "being sent from", info[0],"to",info[1],"\n")
    if(info[2] == "CS"):
        #If its a Caesar cipher input:
        response = processCS(info[3], dictionary)
        if len(response[0]) == 0:
            print("\nNo match was found!")
        elif len(response[0]) == 1:
            print("\nFound a match!")
            print("Match:",response[0][0][0],"using key",response[0][0][1])
            output.append(response[0][0][0] + '\n') #ONLY ADD FIRST RESPONSE TYPE
            print("The average key attempt time was",response[1]/26,"s.")
            print("The 26 key attempts took",response[1],"s.")
            print("The dictionary search took",response[2],"s.")
        elif len(response[0]) > 1:
            print("\nMultiple Matches found!")
            for match in response[0]:
                print("Match:",match[0],"using key",match[1])
            output.append(response[0][0][0] + '\n') #ONLY ADD FIRST RESPONSE TYPE
            print("The average key attempt time was",response[1]/26,"s.")
            print("The 26 key attempts took",response[1],"s.")
            print("The dictionary search took",response[2],"s.")      
        
    else:
        #if its a DES input:
        print("\nAttempting DES bruteforce for", info[3],"...")
        response = processDES(info[3], dictionary, finalKeySet)
        if response[0] == None:
            print("\nNo match was found!")
        elif response[0] != None:
            print("\nFound a match!")
            print("Match:",response[0],"using key",response[1])
            output.append(response[0] + '\n') #add to the output column
            outputtime.append(response[2])
            print("The decrypt took",response[2],"s\n")
        
    print("================================================================================")
    
print("Average DES Time:",sum(outputtime)/4)
    
i = 0
with open("output.txt", 'w') as f:
    for line in commandList:
        f.write(line + ", " + output[i])
        i += 1

print("Finished writing output.txt!\n")
