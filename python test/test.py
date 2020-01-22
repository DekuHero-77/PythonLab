sub = [['0','zero'], ['1','one'], ['2','two'], ['3','three'], ['4','four'], ['5','five'], ['6','six'], ['7','seven'], ['8','eight'], ['9','nine'], ['10','ten']]

def code(message, sub):
    for s in sub:
        vcar = s[0]
        ncar = s[1]
        if '10' in message :              #test pour introduire le "10"
            vcar = '10'
            ncar = 'ten'
        message = message.replace(vcar, ncar)
    return message
message = input()
message.lower()
msg_conv = code(message, sub)
print(msg_conv)