/* Native x87 reference for a bounded owned fixture; no game or host input.
 * FNSTENV masks the deferred exception before returning to C, then FNINIT.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    uint16_t cw = 0x037e; /* only invalid-operation exception unmasked */
    unsigned char env[28] __attribute__((aligned(16)));
    memset(env, 0xa5, sizeof(env));
    __asm__ volatile("fninit\n\tfldcw %1\n\tfldz\n\tfldz\n\t"
                     ".byte 0xde,0xf9\n\tfnstenv %0\n\tfninit"
                     : "=m" (env) : "m" (cw) : "memory", "st", "st(1)");
    return fwrite(env, 1, sizeof(env), stdout) == sizeof(env) ? 0 : 1;
}
