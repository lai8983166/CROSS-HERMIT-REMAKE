/* Project-only stopped RAM/event evidence. GPL-2.0-or-later.
 * Appended to terminal-state.c; no setters and no fabricated guest state.
 */
#include "qemu/rcu.h"
#include "system/ramblock.h"
#include "system/ramlist.h"

TcgStateJson *qmp_x_query_tcg_checkpoint(Error **errp)
{
    CPUState *cs;
    RAMBlock *rb;
    GString *s;
    TcgStateJson *result;
    int i = 0;
    if (!tcg_enabled() || runstate_is_running()) {
        error_setg(errp, "checkpoint observer requires stopped TCG");
        return NULL;
    }
    CPU_FOREACH(cs) {
        if (!cs->stopped) {
            error_setg(errp, "checkpoint observer requires every VP stopped");
            return NULL;
        }
    }
    s = g_string_new("{\"schema\":\"tcg-checkpoint-observation-v1\",\"events\":[");
    CPU_FOREACH(cs) {
        CPUX86State *env = &X86_CPU(cs)->env;
        cpu_synchronize_state(cs);
        if (i++) { g_string_append_c(s, ','); }
        g_string_append_printf(s,
            "{\"cpu\":%d,\"halted\":%u,\"interrupt_request\":%u,"
            "\"exception_index\":%d,\"error_code\":%d,\"exception_is_int\":%d,"
            "\"old_exception\":%d,\"hflags2\":%u,\"exception_next_eip\":",
            cs->cpu_index, cs->halted, cs->interrupt_request,
            cs->exception_index, env->error_code, env->exception_is_int,
            env->old_exception, env->hflags2);
        state_hex(s, env->exception_next_eip);
        g_string_append_c(s, '}');
    }
    g_string_append(s, "],\"ram_blocks\":[");
    i = 0;
    WITH_RCU_READ_LOCK_GUARD() {
        RAMBLOCK_FOREACH(rb) {
            g_autofree char *digest = NULL;
            const char *name = qemu_ram_get_idstr(rb);
            /* Fixed machine block IDs are checked, not inserted unescaped. */
            if (!name || strpbrk(name, "\"\\\n\r") || !rb->host) {
                g_string_free(s, true);
                error_setg(errp, "unsupported RAM block identity or host mapping");
                return NULL;
            }
            digest = g_compute_checksum_for_data(G_CHECKSUM_SHA256,
                                                 rb->host, rb->used_length);
            if (i++) { g_string_append_c(s, ','); }
            g_string_append_printf(s,
                "{\"id\":\"%s\",\"bytes\":%" PRIu64 ","
                "\"migratable\":%s,\"sha256\":\"%s\"}",
                name, (uint64_t)rb->used_length,
                qemu_ram_is_migratable(rb) ? "true" : "false", digest);
        }
    }
    g_string_append(s, "]}");
    result = g_new0(TcgStateJson, 1);
    result->state = g_string_free(s, false);
    return result;
}
