dump = open('dump.txt', 'r').read().split('\n')

# we follow the COMMA address, found by experimenting both 4 address and COMMA address
print(''.join([s.split(',')[3] for s in dump[1:-1] if "COMMA" in s.split(',')[2]])) # the flag