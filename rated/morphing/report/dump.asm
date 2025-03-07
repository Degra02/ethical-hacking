   ...
   0x5555555552b0:	mov    QWORD PTR [rbp-0x8],rdi
   0x5555555552b4:	mov    rax,QWORD PTR [rbp-0x8]
   0x5555555552b8:	movzx  eax,BYTE PTR [rax]
   0x5555555552bb:	cmp    al,0x55                 % comparison with the input
   0x5555555552bd:	je     0x5555555552c9          % jump below
   0x5555555552bf:	mov    eax,0x0
   0x5555555552c4:	jmp    0x5555555555fd
   0x5555555552c9:	mov    rax,QWORD PTR [rbp-0x8]
   0x5555555552cd:	movzx  eax,BYTE PTR [rax]
   0x5555555552d0:	movsx  eax,al
   0x5555555552d3:	mov    edi,eax
   0x5555555552d5:	call   0x555555555189          % call to $decryptor
   ...
