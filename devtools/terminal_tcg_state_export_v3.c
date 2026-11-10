/* Project-local diagnostic endpoint, compiled into the pinned TCG build.
 * GPL-2.0-or-later. CPU state only; not a machine checkpoint/restore format.
 */
#include "qemu/osdep.h"
#include "cpu.h"
#include "qapi/error.h"
#include "qapi/qapi-commands-misc-i386.h"
#include "system/cpus.h"
#include "system/hw_accel.h"
#include "system/runstate.h"
#include "system/tcg.h"

static void state_hex(GString *s, uint64_t value)
{
    g_string_append_printf(s, "\"%016" PRIx64 "\"", value);
}

TcgStateJson *qmp_x_query_tcg_state(int64_t cpu_index, Error **errp)
{
    CPUState *cs, *other;
    CPUX86State *env;
    GString *s;
    TcgStateJson *result;
    int i, j;
    uint32_t empty = 0;
    SegmentCache *seg;

    if (!tcg_enabled() || runstate_is_running()) {
        error_setg(errp, "state-v1 requires stopped TCG");
        return NULL;
    }
    CPU_FOREACH(other) {
        if (!other->stopped) {
            error_setg(errp, "all CPUs must be stopped");
            return NULL;
        }
    }
    if (cpu_index < 0 || cpu_index > INT_MAX ||
        !(cs = qemu_get_cpu(cpu_index))) {
        error_setg(errp, "invalid CPU index");
        return NULL;
    }
    cpu_synchronize_state(cs);
    env = &X86_CPU(cs)->env;
    update_mxcsr_from_sse_status(env);
    s = g_string_new("{\"schema\":\"tcg-state-v1\",\"fullstate_accepted\":false,");
    g_string_append(s, "\"vp_stopped\":[");
    i = 0;
    CPU_FOREACH(other) {
        if (i++) { g_string_append_c(s, ','); }
        g_string_append_printf(s, "{\"cpu\":%d,\"stopped\":%s}",
                               other->cpu_index, other->stopped ? "true" : "false");
    }
    g_string_append(s, "],");
    g_string_append_printf(s, "\"cpu\":%d,\"target_bits\":%d,\"gpr\":[",
                           cs->cpu_index, TARGET_LONG_BITS);
    for (i = 0; i < CPU_NB_REGS; i++) {
        if (i) { g_string_append_c(s, ','); }
        state_hex(s, env->regs[i]);
    }
    g_string_append(s, "],\"eip\":"); state_hex(s, env->eip);
    g_string_append(s, ",\"eflags\":"); state_hex(s, cpu_compute_eflags(env));
    g_string_append(s, ",\"hflags\":"); state_hex(s, env->hflags);
    g_string_append(s, ",\"efer\":"); state_hex(s, env->efer);
    g_string_append(s, ",\"segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt\":[");
    for (i = 0; i < 10; i++) {
        seg = i < 6 ? &env->segs[i] : i == 6 ? &env->ldt :
              i == 7 ? &env->tr : i == 8 ? &env->gdt : &env->idt;
        if (i) { g_string_append_c(s, ','); }
        g_string_append_c(s, '['); state_hex(s, seg->selector);
        g_string_append_c(s, ','); state_hex(s, seg->base);
        g_string_append_c(s, ','); state_hex(s, seg->limit);
        g_string_append_c(s, ','); state_hex(s, seg->flags);
        g_string_append_c(s, ']');
    }
    g_string_append(s, "],\"cr0_cr2_cr3_cr4\":[");
    for (i = 0; i < 4; i++) {
        if (i) { g_string_append_c(s, ','); }
        state_hex(s, env->cr[i ? i + 1 : 0]);
    }
    g_string_append(s, "],\"dr0_dr1_dr2_dr3_dr6_dr7\":[");
    for (i = 0; i < 6; i++) {
        if (i) { g_string_append_c(s, ','); }
        state_hex(s, env->dr[i < 4 ? i : i + 2]);
    }
    g_string_append(s, "],\"dr4_dr5_policy\":\"DE=0 aliases DR6/7; DE=1 undefined, not independent slots\",");
    g_string_append_printf(s, "\"fp_control\":%u,\"fp_status\":%u,\"top\":%u,",
                           env->fpuc, (env->fpus & ~0x3800) | (env->fpstt << 11), env->fpstt);
    g_string_append(s, "\"fp_physical_low64_high16\":[");
    for (i = 0; i < 8; i++) {
        empty |= (env->fptags[i] != 0) << i;
        if (i) { g_string_append_c(s, ','); }
        g_string_append_c(s, '['); state_hex(s, env->fpregs[i].d.low);
        g_string_append_c(s, ','); state_hex(s, env->fpregs[i].d.high);
        g_string_append_c(s, ']');
    }
    g_string_append_printf(s, "],\"fp_empty_mask\":%u,\"fop\":%u,\"fcs\":%u,\"fds\":%u,",
                           empty, env->fpop, env->fpcs, env->fpds);
    g_string_append(s, "\"fip\":"); state_hex(s, env->fpip);
    g_string_append(s, ",\"fdp\":"); state_hex(s, env->fpdp);
    g_string_append_printf(s, ",\"mxcsr\":%u,\"xmm_low64_high64\":[", env->mxcsr);
    for (i = 0; i < CPU_NB_REGS; i++) {
        if (i) { g_string_append_c(s, ','); }
        g_string_append_c(s, '[');
        for (j = 0; j < 2; j++) {
            if (j) { g_string_append_c(s, ','); }
            state_hex(s, env->xmm_regs[i].ZMM_Q(j));
        }
        g_string_append_c(s, ']');
    }
    g_string_append(s, "]}");
    result = g_new0(TcgStateJson, 1);
    result->state = g_string_free(s, false);
    return result;
}
