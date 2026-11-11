/* Owned SMP long-mode microguest. No host architectural writes. */
.section .text
.code32
.align 4
.long 0x1badb002,0,-0x1badb002
.global _start,ctx_arm,ctx_hit,ctx_next,ctx_end
_start:
 cli
 lgdt gdtr
 ljmp $8,$boot32
boot32:
 mov $16,%ax
 mov %ax,%ds
 mov %ax,%es
 mov %ax,%ss
 mov $0x120000,%esp
 cld
 mov $0x110000,%edi
 xor %eax,%eax
 mov $5120,%ecx
 rep stosl
 movl $0x111003,0x110000
 movl $0x111003,0x113000
 movl $0x112003,0x111000
 movl $0x114003,0x111018
 movl $0xfee00083,0x114fb8
 mov $0x112000,%edi
 mov $0x83,%eax
 mov $512,%ecx
1: mov %eax,(%edi)
 add $0x200000,%eax
 add $8,%edi
 loop 1b
 mov $ap_start,%esi
 mov $0x8000,%edi
 mov $(ap_end-ap_start),%ecx
 rep movsb
 jmp common32
common32:
 mov $0x110000,%eax
 mov %eax,%cr3
 mov %cr4,%eax
 or $0x20,%eax
 mov %eax,%cr4
 mov $0xc0000080,%ecx
 rdmsr
 or $0x100,%eax
 wrmsr
 mov %cr0,%eax
 or $0x80000000,%eax
 mov %eax,%cr0
 ljmp $24,$long64
.code64
long64:
 mov $0x1234,%r13
 mov $1,%eax
 cpuid
 shr $24,%ebx
 test %ebx,%ebx
 jnz ap64
 mov $0x120000,%rsp
 /* APIC physical ICR: INIT then SIPI, CPU1 only. */
 mov $0xfee00000,%edx
 movl $0x01000000,0x310(%rdx)
 movl $0x00004500,0x300(%rdx)
2: mov 0x300(%rdx),%eax
 test $0x1000,%eax
 jnz 2b
 movl $0x00004608,0x300(%rdx)
3: cmpl $1,ap_ready
 je 4f
 pause
 jmp 3b
4:
ctx_arm:
 nop
 movl $1,ap_go
6: cmpl $1,ap_done
 jne 6b
 mov $0x113000,%eax
 mov %rax,%cr3
 call ctx_hit
 mov $0x110000,%eax
 mov %rax,%cr3
 inc %r13
 call ctx_hit
 dec %r13
 call ctx_hit
ctx_end:
 nop
 mov $0x43,%al
 out %al,$0xe9
 mov $16,%eax
 out %eax,$0xf4
 hlt
 jmp .-1
ap64:
 mov $0x124000,%rsp
 movl $1,ap_ready
7: cmpl $1,ap_go
 jne 7b
 call ctx_hit
 movl $1,ap_done
5: hlt
 jmp 5b
.align 4096
ctx_hit:
 nop
ctx_next:
 incl hit_count
 ret
.code16
ap_start:
 cli
 xor %ax,%ax
 mov %ax,%ds
 addr32 lgdtl gdtr
 mov %cr0,%eax
 or $1,%eax
 mov %eax,%cr0
 ljmpl $8,$ap32
ap_end:
.code32
ap32:
 mov $16,%ax
 mov %ax,%ds
 mov %ax,%es
 mov %ax,%ss
 mov $0x124000,%esp
 jmp common32
.align 8
gdt:
 .quad 0,0x00cf9b000000ffff,0x00cf93000000ffff,0x00af9b000000ffff
gdtr:
 .word 31
 .long gdt
.align 4
ap_done: .long 0
hit_count: .long 0

ap_ready: .long 0
ap_go: .long 0
