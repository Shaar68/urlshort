BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encode(num, alphabet=BASE62):
    if num == 0:
        return alphabet[0]
    
    arr = []
    base = len(alphabet)
    
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string, alphabet=BASE62):
    base = len(alphabet)
    strlen = len(string)
    num = 0
    
    i = 0
    for char in string:
        power = (strlen - (i + 1))
        num += alphabet.index(char) * (base ** power)
        i += 1
    
    return num