/* Owned hardware x87 reference. No global state/input; no deferred exception
 * escapes into C: FNSTENV masks first and FNINIT runs before fwrite.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    uint16_t cw;
    int zero;
    unsigned char env[28] __attribute__((aligned(16)));
    unsigned char fx[512] __attribute__((aligned(16)));
    if (argc != 2) return 2;
    zero = strstr(argv[1], "zero") != NULL;
    if (!strcmp(argv[1], "invalid-unmasked")) cw=0x037e;
    else if (!strcmp(argv[1], "zero-unmasked")) cw=0x037b;
    else if (!strcmp(argv[1], "invalid-masked") || !strcmp(argv[1], "zero-masked")) cw=0x037f;
    else return 2;
    memset(env, 0xa5, sizeof(env)); memset(fx, 0xa5, sizeof(fx));
    if (zero) {
        __asm__ volatile("fninit\n\tfldcw %2\n\tfld1\n\tfldz\n\t"
                         ".byte 0xde,0xf9\n\tfnstenv %0\n\tfxsave %1\n\tfninit"
                         : "=m" (env), "=m" (fx) : "m" (cw) : "memory", "st", "st(1)");
    } else {
        __asm__ volatile("fninit\n\tfldcw %2\n\tfldz\n\tfldz\n\t"
                         ".byte 0xde,0xf9\n\tfnstenv %0\n\tfxsave %1\n\tfninit"
                         : "=m" (env), "=m" (fx) : "m" (cw) : "memory", "st", "st(1)");
    }
    return fwrite(env,1,sizeof(env),stdout)==sizeof(env) && fwrite(fx,1,sizeof(fx),stdout)==sizeof(fx) ? 0 : 1;
}
