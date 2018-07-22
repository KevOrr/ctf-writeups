# Stegonography - Dissonance

### Description

> Do you hear flag?

### Attachments

[dissonance.zip](dissonance.zip)

### Solution

After reading the description, I thought this would be a spectrogram challenge.
Unzipping the zip file leaves us with a single file, `dissonance.wav`. But
it doesn't seem to be a wav file. Looking at it in a text editor, it looks
like a midi file!

Change the extension from `.wav` to `.midi` and `File > Import > MIDI...` it in
Audacity. The flag is clear as day.

![Audacity Screenshot][audacity.png]

### Flag

    FIT{Jwbx4CtiL8Et}
