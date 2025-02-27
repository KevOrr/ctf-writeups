# B01lers CTF 2020

After a long hiatus playing any CTFs, I had a lot of fun getting back into the
swing of things by playing b01lers CTF, put on by Purdue University.
Unfortunately, I only had the time to look at three of the easier pwning
challenges, and solve two of those.

## Pwn 100 - Department of Flying Vehicles

> Dave ruined the code for the DFV starship registry system. Please help fix it.
>
> `nc pwn.ctf.b01lers.com 1001`  
> [dfv](dfv/dfv)  
> Author: nsnc

This is appears to be a simple keygen/reversing challenge:

```
$ ./dfv
Dave has ruined our system. He updated the code, and now he even has trouble checking his own liscense!
If you can please make it work, we'll reward you!

Welcome to the Department of Flying Vehicles.
Which liscense plate would you like to examine?
 > EATDUST
Error.
```

But when we disassemble it:

![main function of dfv in Binary Ninja](pics/dfv-main.png)

At address `0xabe`, we see that our string is XORed with
`'\x11\x0f\xdcI\xd6\xd5\x04\x10'` (let's call this value `xor`) and then at
address `0xac2` the first 8 bytes are compared to `'R@\x93\x05\x92\x94R\x10'`
(let's call this value `key`). Equivalently, our input is compared to `xor ^
key`, which equals `COOLDAV\0`. If our string matches this value, then
execution continues to a branch were it is possible to reach `sub_96a`, which
prints `flag.txt`. If, on the other hand, our string does not match at all, then
the program exits without printing the flag.

So we know that our input string must be `"COOLDAV"` if we want to print the
flag. Is that all there is to this challenge? A simple XORed string? No! This is
a _100_ point challenge. It better take more than 5 minutes to solve!

If we examine the block starting at `0xad6`, we will see that our same input is
`strncmp`'d with `"COOLDAV"`, and then `sub_96a` is called if our string __does
not match__ with `"COOLDAV"`. So, what can we deduce? We know that our string
must _not_ match `"COOLDAV"`, but _must_ match `"COOLDAV"`. These two
constraints are logical inverses of each other, so requiring both would be
unsatisfiable. In short, the challenge is unsolvable. The end. Thanks for a
wonderful CTF Purdue!

Wait, let's look closer at that `xor` at `0xabe`. Looking at the disassembly, we
can see that `xor` and `key` both live in memory (indeed, there is no version
of the [`xor` instruction on AMD64](https://www.felixcloutier.com/x86/xor) that
can encode a 64-bit immediate operand). In fact, they both live on the stack.
Hmm, if only there were a way to overwrite those two values...

![A closer inspection of instructions 0xab5..0xabe](pics/dfv-closer.png)

Oh, now what's that? A call to `gets`? The
[dangerous](https://stackoverflow.com/q/1694036/1529586),
[unsafe](https://cwe.mitre.org/data/definitions/242.html), and
[deprecated](https://github.com/bminor/glibc/blob/e4a399921390509418826e8e8995d2441f29e243/libio/stdio.h#L571-L582)
`gets`?! Well, now that we know we have a buffer overflow on the stack, we
should be able to overwrite `xor` or `key`, or both! This will allow us to give
an input string that does not match `"COOLDAV"`, and by changing `xor` and
`key`, it can match `xor ^ key`. So we need to choose an `s`, `xor`, and `key`,
such that `s ^ xor == key` and `s != "COOLDAV"`. Solving the challenge is as
simple as sending each in order. See [sol.py](dfv/sol.py) for the full solution.


## Pwn 100 - Meshuggah 2.0

> Dave escaped security, but only by crashing directly into an asteroid. Don't worry, he's still alive, but he's going to need a new starship
>
> `nc pwn.ctf.b01lers.com 1003`  
> [meshuggah](meshuggah/meshuggah)  
> Author: maczilla

When we visit the Used ~~Car~~ Starship Dealer, they inform us of an ongiong
sale: one starship at any time will be 90% off, but it is up to us to identify
it. For accountability, they kinda provide us with the first three starships of
the day that were sold at 90% off, and then we are asked which starship we would
like to buy.

```
Welcome to the Used Car Dealership, we hope you are ready for the insane savings ahead of you!
Here are the first three starships which were purchased today for an incredible 90% savings. Each starship costs a mere 10 credits when on sale, but we only put one on sale at a time

1. Meshuggah-1508316696
2. Meshuggah-1908484246
3. Meshuggah-340538234

I don't even know how Meshuggah comes up with their model names, but I don't care because everyone buys them

Which model starship would you like to buy? 420
Thats gonna be an expensive one... Glad you're buying from me! And please come back after that one breaks down.
```

![main function of meshuggah in Binary Ninja](pics/meshuggah-main.png)

`main` is simple enough: `srand(time(NULL) + 2)`, `list_purchases()`, then it gives
us 1000 money, then calls `buy_starship` 92 times. If we're able to make 92
purchases without go bankrupt, then it will print the flag; otherwise it just
exits.

![list_previous_purchases function of meshuggah in Binary Ninja](pics/meshuggah-list-previous.png)

`list_previous_purchases` prints out the first three random numbers returned by `rand()`.

![buy_starship function of meshuggah in Binary Ninja](pics/meshuggah-buy.png)

`buy_starship` asks us to choose a starship by number, then produces a random
number using `rand()`. If our two numbers match, they sell us the starship
for 10 money; otherwise they sell it for 100 money.

We start with 1000 money, and we need to make 92 purchases. If we pull this off
perfectly, guessing the right number every single time, then we'll wind up
spending 920 (92 * 10). Now it's apparent to me why 92: if we guess wrong even
once, we would have to spend 1010 money to purchase 92 starships. It's set up so
that we have to perfectly guess all 92 starships.

Normally, this would be extremely hard. `rand()` returns an `int`, which on most
systems is a 32-bit number, making it about a 1-in-4-billion chance to correctly
guess any one number, let alone 92 of them. Fortunately, we have two tricks up
our sleeve:

1. We are given the first three numbers that come out of the PRNG, so instead of
   making a 1-in-4-billion chance guess 92 times, we can search through all the
   possible seeds (again, on most systems a 32-bit number) and find the one(s)
   that produce a PRNG sequence that matches the first three given to us.
2. The way that they are seeding the PRNG is very important. Since they are
   seeding it with `time(NULL) + 2`, if we can guess the system time, then we
   can figure out the seed. This is a serious flaw, and corresponds to [CWE
   337](https://cwe.mitre.org/data/definitions/337.html)

(1) alone would be very inefficient (on my machine it would take about an hour),
and it's not guaranteed to give just one result. But when we combine it with
(2), there might only be a few seeds that we have to search, due to any
uncertainty in the system time.

So, to wrap up, we need to collect the three initial PRNG values leaked to us.
Then we try seeds that are near `time(NULL) + 2` until we find one that produces
a sequence that starts with those three numbers. Then, using that seed, we send
the next 92 numbers to the target. See [sol.py](meshuggah/sol.py) for the full
solution.
