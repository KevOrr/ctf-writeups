# Mix - Complex Problem

### Description

> Can you solve this problem?

### Attachments

[img.bmp](img.bmp)

### Solution

Delete everything until last null byte (^@), first line should start with f now.

    base64 -d img.bmp >prog
    upx -d prog
