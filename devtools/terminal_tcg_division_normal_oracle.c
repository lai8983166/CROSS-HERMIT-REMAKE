#include <stdint.h>
#include <stdio.h>
#include <string.h>
int main(int argc,char **argv)
{
    uint16_t cw=0x037f;
    float eight=8.0f,two=2.0f;
    unsigned char env[28] __attribute__((aligned(16)));
    unsigned char fx[512] __attribute__((aligned(16)));
    if(argc!=2)return 2;
    memset(env,0xa5,sizeof(env));memset(fx,0xa5,sizeof(fx));
    if(!strcmp(argv[1],"normal-forward")) {
        __asm__ volatile("fninit; fldcw %2; flds %3; flds %4; .byte 0xde,0xf9; fnstenv %0; fxsave %1; fninit"
            : "=m"(env),"=m"(fx) : "m"(cw),"m"(eight),"m"(two) : "memory","st","st(1)");
    } else if(!strcmp(argv[1],"normal-reverse")) {
        __asm__ volatile("fninit; fldcw %2; flds %3; flds %4; .byte 0xde,0xf1; fnstenv %0; fxsave %1; fninit"
            : "=m"(env),"=m"(fx) : "m"(cw),"m"(eight),"m"(two) : "memory","st","st(1)");
    } else return 2;
    return fwrite(env,1,sizeof(env),stdout)==sizeof(env)&&fwrite(fx,1,sizeof(fx),stdout)==sizeof(fx)?0:1;
}
