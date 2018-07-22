# Stegonography - Hide Flag

### Description

> Flag is in the image.

### Attachments

[flag.png](flag.png)

### Solution

Opening the image in GIMP shows a seemingly completely white square. Selecting
the "Select by Color" tool and turning the threshold down to 0 tells us
otherwise however. Using the tool on any part of the image selects only about
half of the pixels. By using the eyedropper tool, it is revealed that about half
of the pixels are `#ffffff` (white) and about half are `#fefefe` (one less than
fully bright in each rgb channel).

By selecting the non-white pixels and turning them completely black, we reveal
what appears to be a QR code ([flag_enhanced.png](flag_enhanced.png)). Any QR
code reader can reveal the contents of the message.

### Flag

    FIT{rtuw8Enj8f2D}
