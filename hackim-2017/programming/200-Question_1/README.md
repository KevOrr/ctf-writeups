# Programming 200 - Question 1 (abc)

### Description

> We unearthed this text file from one of the older servers and want to know
> what this is all about. Could you please analyse this and let us know your
> finding?

### Included Files/Servers

* `abc.txt`

### Solution

tl;dr solution in `sol.py`

`abc.txt` is a string representation of an array. Each value is between 190 and
255. These seem to be 8-bit rgb values. Passing the file into `numpy`, we can
see that the length of the array is 1585803. Dividing this by 3 gives 528601
pixels. Passing this into a prime factorization calculator, we see the only
factors of 528601 are 929 and 569.

If we reshape the numpy array into the shape `(929, 569, 3)`, read the reshaped
view of the array into the python library `pillow` (a derivative of `PIL`),
and output the image into `flag.png`, the somewhat apropros flag will be
visible.

### Flag

    flag{PiL_PIL_PIL}
