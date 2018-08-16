## Junior 20 - Salad Upgrades

> Sure, I could toss them all using just one shift. But am I gonna?
> 
> CIPHERTEXT: e4uo{zo1b_1e_f0j4l10i}z0ce


### Solution

    plain = ''
    ciphertext = 'e4uo{zo1b_1e_f0j4l10i}z0ce'
    for c, offset in zip(ciphertext, range(1, 100)):
    if c in string.ascii_lowercase:
        plain += chr((ord(c) - ord('a') - i) % 26 + ord('a'))
    else:
        plains += c
