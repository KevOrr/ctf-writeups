# Binary - Number

### Description

> Number is beautiful

### Attachments

[number](number)

### Solution

Disassembling `main()`, we get:

    000000000040064d <main>:
      40064d:       55                      push   rbp
      40064e:       48 89 e5                mov    rbp,rsp
      400651:       48 83 ec 20             sub    rsp,0x20
      400655:       c7 45 f0 00 00 00 00    mov    DWORD PTR [rbp-0x10],0x0
      40065c:       c6 45 ff 46             mov    BYTE PTR [rbp-0x1],0x46
      400660:       c6 45 fe 54             mov    BYTE PTR [rbp-0x2],0x54
      400664:       c6 45 fd 63             mov    BYTE PTR [rbp-0x3],0x63
      400668:       c6 45 fc 49             mov    BYTE PTR [rbp-0x4],0x49
      40066c:       c6 45 fb 7b             mov    BYTE PTR [rbp-0x5],0x7b
      400670:       c7 45 e0 32 2e 37 31    mov    DWORD PTR [rbp-0x20],0x31372e32
      400677:       66 c7 45 e4 38 32       mov    WORD PTR [rbp-0x1c],0x3238
      40067d:       c6 45 e6 00             mov    BYTE PTR [rbp-0x1a],0x0
      400681:       c6 45 fa 38             mov    BYTE PTR [rbp-0x6],0x38
      400685:       c6 45 f9 31             mov    BYTE PTR [rbp-0x7],0x31
      400689:       c6 45 f8 38             mov    BYTE PTR [rbp-0x8],0x38
      40068d:       c6 45 f7 32             mov    BYTE PTR [rbp-0x9],0x32
      400691:       c6 45 f6 38             mov    BYTE PTR [rbp-0xa],0x38
      400695:       c6 45 f5 7d             mov    BYTE PTR [rbp-0xb],0x7d
      400699:       bf f4 07 40 00          mov    edi,0x4007f4
      40069e:       e8 6d fe ff ff          call   400510 <puts@plt>
      4006a3:       48 8d 45 f0             lea    rax,[rbp-0x10]
      4006a7:       48 89 c6                mov    rsi,rax
      4006aa:       bf 12 08 40 00          mov    edi,0x400812
      4006af:       b8 00 00 00 00          mov    eax,0x0
      4006b4:       e8 87 fe ff ff          call   400540 <__isoc99_scanf@plt>
      4006b9:       8b 45 f0                mov    eax,DWORD PTR [rbp-0x10]
      4006bc:       83 e8 1a                sub    eax,0x1a
      4006bf:       89 45 f0                mov    DWORD PTR [rbp-0x10],eax
      4006c2:       8b 45 f0                mov    eax,DWORD PTR [rbp-0x10]
      4006c5:       3d 66 04 00 00          cmp    eax,0x466
      4006ca:       0f 85 86 00 00 00       jne    400756 <main+0x109>
      4006d0:       0f be 45 ff             movsx  eax,BYTE PTR [rbp-0x1]
      4006d4:       89 c7                   mov    edi,eax
      4006d6:       e8 25 fe ff ff          call   400500 <putchar@plt>
      4006db:       0f be 45 fc             movsx  eax,BYTE PTR [rbp-0x4]
      4006df:       89 c7                   mov    edi,eax
      4006e1:       e8 1a fe ff ff          call   400500 <putchar@plt>
      4006e6:       0f be 45 fe             movsx  eax,BYTE PTR [rbp-0x2]
      4006ea:       89 c7                   mov    edi,eax
      4006ec:       e8 0f fe ff ff          call   400500 <putchar@plt>
      4006f1:       0f be 45 fb             movsx  eax,BYTE PTR [rbp-0x5]
      4006f5:       89 c7                   mov    edi,eax
      4006f7:       e8 04 fe ff ff          call   400500 <putchar@plt>
      4006fc:       48 8d 45 e0             lea    rax,[rbp-0x20]
      400700:       48 89 c6                mov    rsi,rax
      400703:       bf 15 08 40 00          mov    edi,0x400815
      400708:       b8 00 00 00 00          mov    eax,0x0
      40070d:       e8 0e fe ff ff          call   400520 <printf@plt>
      400712:       0f be 45 f8             movsx  eax,BYTE PTR [rbp-0x8]
      400716:       89 c7                   mov    edi,eax
      400718:       e8 e3 fd ff ff          call   400500 <putchar@plt>
      40071d:       0f be 45 f9             movsx  eax,BYTE PTR [rbp-0x7]
      400721:       89 c7                   mov    edi,eax
      400723:       e8 d8 fd ff ff          call   400500 <putchar@plt>
      400728:       0f be 45 f6             movsx  eax,BYTE PTR [rbp-0xa]
      40072c:       89 c7                   mov    edi,eax
      40072e:       e8 cd fd ff ff          call   400500 <putchar@plt>
      400733:       0f be 45 f7             movsx  eax,BYTE PTR [rbp-0x9]
      400737:       89 c7                   mov    edi,eax
      400739:       e8 c2 fd ff ff          call   400500 <putchar@plt>
      40073e:       0f be 45 fa             movsx  eax,BYTE PTR [rbp-0x6]
      400742:       89 c7                   mov    edi,eax
      400744:       e8 b7 fd ff ff          call   400500 <putchar@plt>
      400749:       0f be 45 f5             movsx  eax,BYTE PTR [rbp-0xb]
      40074d:       89 c7                   mov    edi,eax
      40074f:       e8 ac fd ff ff          call   400500 <putchar@plt>
      400754:       eb 0a                   jmp    400760 <main+0x113>
      400756:       bf 18 08 40 00          mov    edi,0x400818
      40075b:       e8 b0 fd ff ff          call   400510 <puts@plt>
      400760:       b8 00 00 00 00          mov    eax,0x0
      400765:       c9                      leave  
      400766:       c3                      ret    
      400767:       66 0f 1f 84 00 00 00    nop    WORD PTR [rax+rax*1+0x0]
      40076e:       00 00 

This challenge can be solved in one of two ways:

1. Here, the code between `4006aa` and `4006ca` is especially important.
   At `4006b4`, we call `scanf("%d", &some_var)` to obtain a single int
   from user input. At `4006bc`, we subtract `0x1a` (i.e. 26) from that
   number, and then compare the result to `0x466` (1126) at `4006c5`.
   
   If they are equal, at `4006ca` we take the positive branch which leads
   to some code that prints the flag. And if not, we take the negative
   branch which prints "No." and exits.
   
   So what number should we input? Well, we know that the number has to
   equal 1126 at the end, but that's after 26 has been subtracted. So
   the number must be 1152.
   
   Entering this number into the running program reveals the flag.
   
2. The code between `400655` and `400695` sets many stack variables. These
   are later used in the positive branch starting at `4006d0`. In the order
   they are printed out, we're looking at:
   
       46 49 54 7b 31 37 2e 32 32 38 38 31 38 38 32 38 7d
   
   Ascii decoding this string reveals the flag
   
### Flag

    FIT{17.228818838}
