4919f0: push ebp
4919f1: mov ebp, esp
4919f3: sub esp, 0x64
4919f6: push ebx
4919f7: push esi
4919f8: push edi
4919f9: push ecx
4919fa: lea edi, [ebp - 0x64]
4919fd: mov ecx, 0x19
491a02: mov eax, 0xcccccccc
491a07: rep stosd dword ptr es:[edi], eax
491a09: pop ecx
491a0a: mov dword ptr [ebp - 4], ecx
491a0d: mov eax, dword ptr [ebp + 0x10]
491a10: xor ecx, ecx
491a12: mov cl, byte ptr [eax + 2]
491a15: test ecx, ecx
491a17: jl 0x491a28
491a19: mov edx, dword ptr [ebp + 0x10]
491a1c: xor eax, eax
491a1e: mov al, byte ptr [edx + 2]
491a21: cmp eax, 0xfa
491a26: jl 0x491a4c
491a28: push 0
491a2a: movsx ecx, word ptr [0x619240]
491a31: add ecx, 6
491a34: push ecx
491a35: push 0x59e5d0
491a3a: push 0x59d980
491a3f: call 0x424f80   ; FUN_424f80
491a44: add esp, 0x10
491a47: test eax, eax
491a49: je 0x491a4c
491a4b: int3 
491a4c: mov edx, dword ptr [ebp + 0x10]
491a4f: xor eax, eax
491a51: mov al, byte ptr [edx + 3]
491a54: test eax, eax
491a56: jl 0x491a68
491a58: mov ecx, dword ptr [ebp + 0x10]
491a5b: xor edx, edx
491a5d: mov dl, byte ptr [ecx + 3]
491a60: cmp edx, 0xfa
491a66: jl 0x491a8c
491a68: push 0
491a6a: movsx eax, word ptr [0x619240]
491a71: add eax, 7
491a74: push eax
491a75: push 0x59e5d0
491a7a: push 0x59d95c
491a7f: call 0x424f80   ; FUN_424f80
491a84: add esp, 0x10
491a87: test eax, eax
491a89: je 0x491a8c
491a8b: int3 
491a8c: mov ecx, dword ptr [ebp + 0x10]
491a8f: xor edx, edx
491a91: mov dl, byte ptr [ecx + 2]
491a94: imul edx, edx, 0x520
491a9a: mov eax, dword ptr [ebp - 4]
491a9d: lea ecx, [eax + edx + 0x80aec]
491aa4: mov dword ptr [ebp - 8], ecx
491aa7: mov edx, dword ptr [ebp + 0x10]
491aaa: xor eax, eax
491aac: mov al, byte ptr [edx + 3]
491aaf: imul eax, eax, 0x520
491ab5: mov ecx, dword ptr [ebp - 4]
491ab8: lea edx, [ecx + eax + 0x80aec]
491abf: mov dword ptr [ebp - 0xc], edx
491ac2: mov eax, dword ptr [ebp - 8]
491ac5: push eax
491ac6: mov ecx, dword ptr [ebp - 4]
491ac9: call 0x4690a0   ; FUN_4690a0
491ace: test eax, eax
491ad0: je 0x491adc
491ad2: mov eax, 1
491ad7: jmp 0x491ea9
491adc: mov ecx, dword ptr [ebp - 0xc]
491adf: push ecx
491ae0: mov ecx, dword ptr [ebp - 4]
491ae3: call 0x4690a0   ; FUN_4690a0
491ae8: test eax, eax
491aea: je 0x491af6
491aec: mov eax, 1
491af1: jmp 0x491ea9
491af6: mov edx, dword ptr [ebp + 0x10]
491af9: movzx ax, byte ptr [edx + 2]
491afe: mov ecx, dword ptr [ebp + 8]
491b01: mov edx, dword ptr [ecx + 0x258]
491b07: mov word ptr [edx + 0xa6], ax
491b0e: mov eax, dword ptr [ebp - 0xc]
491b11: mov ecx, dword ptr [eax + 0x258]
491b17: xor edx, edx
491b19: mov dx, word ptr [ecx + 0xc]
491b1d: mov dword ptr [ebp - 0x18], edx
491b20: cmp dword ptr [ebp - 0x18], 0x1c6
491b27: je 0x491b34
491b29: cmp dword ptr [ebp - 0x18], 0x1c7
491b30: je 0x491b69
491b32: jmp 0x491b9c
491b34: mov eax, dword ptr [ebp + 0x10]
491b37: movsx ecx, word ptr [eax + 4]
491b3b: cmp ecx, 0x64
491b3e: jge 0x491b67
491b40: mov edx, dword ptr [ebp + 0x10]
491b43: xor eax, eax
491b45: mov al, byte ptr [edx + 6]
491b48: cmp eax, 4
491b4b: je 0x491b5d
491b4d: push 0
491b4f: push 0
491b51: mov ecx, dword ptr [ebp - 0xc]
491b54: push ecx
491b55: mov ecx, dword ptr [ebp - 4]
491b58: call 0x493090   ; FUN_493090
491b5d: mov eax, 1
491b62: jmp 0x491ea9
491b67: jmp 0x491b9c
491b69: mov edx, dword ptr [ebp + 0x10]
491b6c: movsx eax, word ptr [edx + 4]
491b70: cmp eax, 0x64
491b73: jl 0x491b9c
491b75: mov ecx, dword ptr [ebp + 0x10]
491b78: xor edx, edx
491b7a: mov dl, byte ptr [ecx + 6]
491b7d: cmp edx, 4
491b80: je 0x491b92
491b82: push 0
491b84: push 0
491b86: mov eax, dword ptr [ebp - 0xc]
491b89: push eax
491b8a: mov ecx, dword ptr [ebp - 4]
491b8d: call 0x493090   ; FUN_493090
491b92: mov eax, 1
491b97: jmp 0x491ea9
491b9c: mov ecx, dword ptr [ebp + 0x10]
491b9f: movsx edx, word ptr [ecx + 4]
491ba3: mov dword ptr [ebp - 0x1c], edx
491ba6: mov eax, dword ptr [ebp + 0x10]
491ba9: push eax
491baa: mov ecx, dword ptr [ebp - 0xc]
491bad: push ecx
491bae: mov edx, dword ptr [ebp - 8]
491bb1: push edx
491bb2: mov ecx, dword ptr [ebp - 4]
491bb5: call 0x491ef0   ; FUN_491ef0
491bba: mov eax, dword ptr [ebp + 8]
491bbd: push eax
491bbe: mov ecx, dword ptr [ebp - 4]
491bc1: call 0x469b90   ; FUN_469b90
491bc6: test eax, eax
491bc8: je 0x491bd4
491bca: mov eax, 1
491bcf: jmp 0x491ea9
491bd4: mov ecx, dword ptr [ebp + 8]
491bd7: push ecx
491bd8: mov ecx, dword ptr [ebp - 4]
491bdb: call 0x469c60   ; FUN_469c60
491be0: test eax, eax
491be2: je 0x491bee
491be4: mov eax, 1
491be9: jmp 0x491ea9
491bee: mov edx, dword ptr [ebp + 0x10]
491bf1: xor eax, eax
491bf3: mov al, byte ptr [edx + 6]
491bf6: mov dword ptr [ebp - 0x20], eax
491bf9: cmp dword ptr [ebp - 0x20], 4
491bfd: ja 0x491ea0
491c03: mov ecx, dword ptr [ebp - 0x20]
491c06: jmp dword ptr [ecx*4 + 0x491ebc]
491c0d: push 0x94
491c12: mov edx, dword ptr [ebp + 8]
491c15: push edx
491c16: mov ecx, dword ptr [ebp - 4]
491c19: call 0x49ad90   ; FUN_49ad90
491c1e: mov eax, dword ptr [ebp + 0x10]
491c21: movsx ecx, word ptr [eax + 0xa]
491c25: test ecx, ecx
491c27: jg 0x491c3a
491c29: push 0x95
491c2e: mov edx, dword ptr [ebp + 8]
491c31: push edx
491c32: mov ecx, dword ptr [ebp - 4]
491c35: call 0x49ad90   ; FUN_49ad90
491c3a: mov eax, dword ptr [ebp - 0xc]
491c3d: mov ecx, dword ptr [ebp - 8]
491c40: mov dx, word ptr [ecx + 2]
491c44: mov word ptr [eax + 0x4fa], dx
491c4b: jmp 0x491ea0
491c50: mov eax, dword ptr [ebp + 0x10]
491c53: movsx ecx, word ptr [eax + 0xa]
491c57: test ecx, ecx
491c59: jg 0x491c69
491c5b: push 0x6c
491c5d: mov edx, dword ptr [ebp + 8]
491c60: push edx
491c61: mov ecx, dword ptr [ebp - 4]
491c64: call 0x49ad90   ; FUN_49ad90
491c69: mov eax, dword ptr [ebp + 8]
491c6c: push eax
491c6d: mov ecx, dword ptr [ebp - 4]
491c70: call 0x4692e0   ; FUN_4692e0
491c75: test eax, eax
491c77: jne 0x491cc8
491c79: mov ecx, dword ptr [ebp + 8]
491c7c: push ecx
491c7d: mov ecx, dword ptr [ebp - 4]
491c80: call 0x469730   ; FUN_469730
491c85: test eax, eax
491c87: jne 0x491c95
491c89: mov edx, dword ptr [ebp + 8]
491c8c: push edx
491c8d: mov ecx, dword ptr [ebp - 4]
491c90: call 0x4753f0   ; FUN_4753f0
491c95: push 0
491c97: mov eax, dword ptr [ebp + 8]
491c9a: push eax
491c9b: mov ecx, dword ptr [ebp - 4]
491c9e: add ecx, 0x2a634
491ca4: call 0x437d90   ; FUN_437d90
491ca9: push 8
491cab: mov ecx, dword ptr [ebp + 8]
491cae: push ecx
491caf: mov ecx, dword ptr [ebp - 4]
491cb2: call 0x475270   ; FUN_475270
491cb7: mov edx, dword ptr [ebp + 8]
491cba: mov eax, dword ptr [ebp - 8]
491cbd: mov cx, word ptr [eax + 2]
491cc1: mov word ptr [edx + 0x4f8], cx
491cc8: mov edx, dword ptr [ebp - 0xc]
491ccb: push edx
491ccc: mov eax, dword ptr [ebp - 8]
491ccf: push eax
491cd0: mov ecx, dword ptr [ebp - 4]
491cd3: call 0x492de0   ; FUN_492de0
491cd8: jmp 0x491ea0
491cdd: mov ecx, dword ptr [ebp + 0x10]
491ce0: movsx edx, word ptr [ecx + 0xa]
491ce4: test edx, edx
491ce6: jg 0x491cf6
491ce8: push 0x6d
491cea: mov eax, dword ptr [ebp + 8]
491ced: push eax
491cee: mov ecx, dword ptr [ebp - 4]
491cf1: call 0x49ad90   ; FUN_49ad90
491cf6: movsx ecx, word ptr [0x7f4488]
491cfd: cmp ecx, 7
491d00: je 0x491d0e
491d02: movsx edx, word ptr [0x7f4488]
491d09: cmp edx, 0x4c
491d0c: jne 0x491d3d
491d0e: mov eax, dword ptr [ebp + 8]
491d11: mov ecx, dword ptr [eax + 0x258]
491d17: xor edx, edx
491d19: mov dx, word ptr [ecx + 2]
491d1d: cmp edx, 6
491d20: jne 0x491d3d
491d22: mov eax, dword ptr [ebp + 8]
491d25: mov ecx, dword ptr [eax + 0x258]
491d2b: xor edx, edx
491d2d: mov dl, byte ptr [ecx + 0xa4]
491d33: cmp edx, 4
491d36: jne 0x491d3d
491d38: jmp 0x491ea7
491d3d: mov eax, dword ptr [ebp + 8]
491d40: push eax
491d41: mov ecx, dword ptr [ebp - 4]
491d44: call 0x4692e0   ; FUN_4692e0
491d49: test eax, eax
491d4b: jne 0x491e64
491d51: mov ecx, dword ptr [ebp + 8]
491d54: push ecx
491d55: mov ecx, dword ptr [ebp - 4]
491d58: call 0x469730   ; FUN_469730
491d5d: test eax, eax
491d5f: jne 0x491d6d
491d61: mov edx, dword ptr [ebp + 8]
491d64: push edx
491d65: mov ecx, dword ptr [ebp - 4]
491d68: call 0x4753f0   ; FUN_4753f0
491d6d: push 0
491d6f: mov eax, dword ptr [ebp + 8]
491d72: push eax
491d73: mov ecx, dword ptr [ebp - 4]
491d76: add ecx, 0x2a634
491d7c: call 0x437d90   ; FUN_437d90
491d81: mov ecx, dword ptr [ebp - 0xc]
491d84: mov edx, dword ptr [ecx + 0x258]
491d8a: xor eax, eax
491d8c: mov ax, word ptr [edx + 0xc]
491d90: shl eax, 6
491d93: add eax, 0x6b2d88
491d98: mov dword ptr [ebp - 0x10], eax
491d9b: mov ecx, dword ptr [ebp - 0x10]
491d9e: xor edx, edx
491da0: mov dl, byte ptr [ecx + 0x21]
491da3: cmp edx, 0x64
491da6: jne 0x491db7
491da8: mov eax, dword ptr [ebp + 8]
491dab: mov byte ptr [eax + 0x4f6], 0xff
491db2: jmp 0x491e45
491db7: mov ecx, dword ptr [ebp + 0x10]
491dba: movsx edx, word ptr [ecx + 4]
491dbe: push edx
491dbf: mov ecx, dword ptr [ebp - 4]
491dc2: call 0x46c9f0   ; FUN_46c9f0
491dc7: test eax, eax
491dc9: je 0x491dd7
491dcb: mov eax, dword ptr [ebp + 8]
491dce: mov byte ptr [eax + 0x4f6], 1
491dd5: jmp 0x491e45
491dd7: mov ecx, dword ptr [ebp + 0x10]
491dda: movsx edx, word ptr [ecx + 4]
491dde: imul edx, edx, 0x48
491de1: add edx, 0x6c2dc8
491de7: mov dword ptr [ebp - 0x14], edx
491dea: mov eax, dword ptr [ebp - 0x14]
491ded: xor ecx, ecx
491def: mov cl, byte ptr [eax + 0x18]
491df2: mov dword ptr [ebp - 0x24], ecx
491df5: cmp dword ptr [ebp - 0x24], 6
491df9: ja 0x491e45
491dfb: mov edx, dword ptr [ebp - 0x24]
491dfe: jmp dword ptr [edx*4 + 0x491ed0]
491e05: mov eax, dword ptr [ebp + 8]
491e08: mov byte ptr [eax + 0x4f6], 0xff
491e0f: jmp 0x491e45
491e11: mov ecx, dword ptr [ebp + 8]
491e14: mov edx, dword ptr [ebp + 0x10]
491e17: mov al, byte ptr [edx + 8]
491e1a: mov byte ptr [ecx + 0x4f4], al
491e20: mov ecx, dword ptr [ebp + 8]
491e23: mov edx, dword ptr [ebp + 0x10]
491e26: mov al, byte ptr [edx + 9]
491e29: mov byte ptr [ecx + 0x4f5], al
491e2f: mov ecx, dword ptr [ebp + 8]
491e32: mov byte ptr [ecx + 0x4f6], 0
491e39: jmp 0x491e45
491e3b: mov edx, dword ptr [ebp + 8]
491e3e: mov byte ptr [edx + 0x4f6], 1
491e45: push 9
491e47: mov eax, dword ptr [ebp + 8]
491e4a: push eax
491e4b: mov ecx, dword ptr [ebp - 4]
491e4e: call 0x475270   ; FUN_475270
491e53: mov ecx, dword ptr [ebp + 8]
491e56: mov edx, dword ptr [ebp - 8]
491e59: mov ax, word ptr [edx + 2]
491e5d: mov word ptr [ecx + 0x4f8], ax
491e64: mov ecx, dword ptr [ebp - 0xc]
491e67: push ecx
491e68: mov edx, dword ptr [ebp - 8]
491e6b: push edx
491e6c: mov ecx, dword ptr [ebp - 4]
491e6f: call 0x492de0   ; FUN_492de0
491e74: jmp 0x491ea0
491e76: push 0x6e
491e78: mov eax, dword ptr [ebp + 8]
491e7b: push eax
491e7c: mov ecx, dword ptr [ebp - 4]
491e7f: call 0x49ad90   ; FUN_49ad90
491e84: mov ecx, dword ptr [ebp + 8]
491e87: push ecx
491e88: mov ecx, dword ptr [ebp - 4]
491e8b: call 0x495050   ; FUN_495050
491e90: mov edx, dword ptr [ebp - 0xc]
491e93: push edx
491e94: mov eax, dword ptr [ebp - 8]
491e97: push eax
491e98: mov ecx, dword ptr [ebp - 4]
491e9b: call 0x492de0   ; FUN_492de0
491ea0: mov eax, 1
491ea5: jmp 0x491ea9
491ea7: jmp 0x491e64
491ea9: pop edi
491eaa: pop esi
491eab: pop ebx
491eac: add esp, 0x64
491eaf: cmp ebp, esp
491eb1: call 0x56ce80   ; FUN_56ce80
491eb6: mov esp, ebp
491eb8: pop ebp
491eb9: ret 0xc
491ebc: or eax, 0x1e00491c
491ec1: sbb al, 0x49
491ec3: add byte ptr [eax + 0x1c], dl
491ec6: dec ecx
491ec7: add ch, bl
491ec9: sbb al, 0x49
491ecb: add byte ptr [esi + 0x1e], dh
491ece: dec ecx
491ecf: add byte ptr [0x3b00491e], al
491ed5: push ds
491ed6: dec ecx
491ed7: add byte ptr [ebx], bh
491ed9: push ds
491eda: dec ecx
491edb: add byte ptr [ebx], bh
491edd: push ds
491ede: dec ecx
491edf: add byte ptr [ecx], dl
491ee1: push ds
491ee2: dec ecx
491ee3: add byte ptr [0x3b00491e], al
491ee9: push ds
491eea: dec ecx
491eeb: add ah, cl
491eed: int3 
491eee: int3 
491eef: int3 