# Misc 20 - NOP

Tags: Trivia

### Description

x86's NOP is actually another instruction. What is the Intel syntax representation of the assembly of the other instruction?

Include a space between operands, if applicable.

### Solution

According to [this page](http://x86.renejeschke.de/html/file_module_x86_id_217.html),
the x86 assembly `NOP` instruction is actually an alias for `xchg eax, eax`.

### Flag

    xchg eax, eax
