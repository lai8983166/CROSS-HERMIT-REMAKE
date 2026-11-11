/* Bounded diagnostic GDB context filter; GPL-2.0-or-later.
 * Guest architectural state is never written. Included by terminal-state.c. */
#define CTX_POINTS 32
#define CTX_MATCHES 1000000
static GMutex ctx_lock;
static bool ctx_active, ctx_poisoned;
static const char *ctx_reason = "";
static uint64_t ctx_cr3, ctx_r13, ctx_points[CTX_POINTS];
static unsigned ctx_npoints;
static uint64_t ctx_accepted, ctx_rejected, ctx_cpu_rejected,
                ctx_cr3_rejected, ctx_r13_rejected;
static int64_t ctx_begin;
static QEMUTimer *ctx_timer;
static void ctx_fail_locked(const char *reason)
{
    if (!ctx_poisoned) { ctx_reason = reason; }
    ctx_poisoned = true;
    qemu_system_vmstop_request_prepare();
    qemu_system_vmstop_request(RUN_STATE_PAUSED);
}
void terminal_context_poison(const char *reason)
{
    g_mutex_lock(&ctx_lock);
    if (ctx_active) { ctx_fail_locked(reason); }
    g_mutex_unlock(&ctx_lock);
}
static void ctx_expired(void *unused)
{
    terminal_context_poison("timeout");
}
bool terminal_context_match(CPUState *cpu, uint64_t pc)
{
    CPUX86State *env = &X86_CPU(cpu)->env;
    bool match = true;
    unsigned i;
    g_mutex_lock(&ctx_lock);
    if (!ctx_active) { goto end; }
    for (i = 0; i < ctx_npoints && ctx_points[i] != pc; i++) { }
    if (i == ctx_npoints) { goto end; }
    if (qemu_clock_get_ns(QEMU_CLOCK_REALTIME) - ctx_begin >= 60000000000LL) {
        ctx_fail_locked("timeout");
    }
    if (ctx_accepted + ctx_rejected >= CTX_MATCHES) {
        ctx_fail_locked("match-budget");
    }
    if (ctx_poisoned) { goto end; } /* stop visibly, never silently bypass */
    match = cpu->cpu_index == 0 && env->cr[3] == ctx_cr3 && env->regs[13] == ctx_r13;
    if (match) { ctx_accepted++; }
    else {
        ctx_rejected++;
        if (cpu->cpu_index != 0) { ctx_cpu_rejected++; }
        if (env->cr[3] != ctx_cr3) { ctx_cr3_rejected++; }
        if (env->regs[13] != ctx_r13) { ctx_r13_rejected++; }
    }
end:
    g_mutex_unlock(&ctx_lock);
    return match;
}
static TcgStateJson *terminal_context_command(int64_t command, Error **errp)
{
    CPUState *cpu;
    CPUBreakpoint *bp;
    int n = 0;
    unsigned count = 0, i;
    uint64_t points[CTX_POINTS];
    TcgStateJson *result;
    GString *s;
    if (!tcg_enabled() || runstate_is_running()) {
        error_setg(errp, "context requires stopped TCG"); return NULL;
    }
    CPU_FOREACH(cpu) {
        if (!cpu->stopped || cpu->cpu_index < 0 || cpu->cpu_index > 1) {
            error_setg(errp, "context requires both CPUs stopped"); return NULL;
        }
        n++;
    }
    if (n != 2) { error_setg(errp, "context requires two CPUs"); return NULL; }
    if (command == -4 || command == -7) {
        if (ctx_poisoned || (command == -4 ? ctx_active : !ctx_active)) {
            error_setg(errp, "context invalid active/poisoned state"); return NULL;
        }
        QTAILQ_FOREACH(bp, &qemu_get_cpu(0)->breakpoints, entry) {
            if (!(bp->flags & BP_GDB)) { continue; }
            for (i = 0; i < count && points[i] != bp->pc; i++) { }
            if (i != count) { continue; }
            if (count == CTX_POINTS) {
                error_setg(errp, "context breakpoint budget"); return NULL;
            }
            points[count++] = bp->pc;
        }
        if (!count) { error_setg(errp, "context needs GDB breakpoints"); return NULL; }
        /* Require exact same configured addresses on the other CPU. */
        n = 0;
        QTAILQ_FOREACH(bp, &qemu_get_cpu(1)->breakpoints, entry) {
            if (!(bp->flags & BP_GDB)) { continue; }
            for (i = 0; i < count && points[i] != bp->pc; i++) { }
            if (i == count) { error_setg(errp, "context asymmetric points"); return NULL; }
            n++;
        }
        if (n != count) { error_setg(errp, "context asymmetric points"); return NULL; }
        memcpy(ctx_points, points, count * sizeof(points[0])); ctx_npoints = count;
        if (command == -4) {
            CPUX86State *env = &X86_CPU(qemu_get_cpu(0))->env;
            ctx_cr3 = env->cr[3]; ctx_r13 = env->regs[13];
            ctx_accepted = ctx_rejected = ctx_cpu_rejected = ctx_cr3_rejected = ctx_r13_rejected = 0;
            ctx_begin = qemu_clock_get_ns(QEMU_CLOCK_REALTIME);
            ctx_active = true;
            if (!ctx_timer) { ctx_timer = timer_new_ns(QEMU_CLOCK_REALTIME, ctx_expired, NULL); }
            timer_mod_ns(ctx_timer, ctx_begin + 60000000000LL);
        }
    } else if (command == -5) {
        if (!ctx_active) { error_setg(errp, "context not active"); return NULL; }
        ctx_active = false; timer_del(ctx_timer);
    }
    result = g_new0(TcgStateJson, 1);
    s = g_string_new(NULL);
    g_string_append_printf(s, "{\"schema\":\"tcg-context-v1\",\"active\":%s,\"poisoned\":%s,"
        "\"reason\":\"%s\",\"cpu\":0,\"cr3\":\"%016" PRIx64 "\",\"r13\":\"%016" PRIx64
        "\",\"accepted\":%" PRIu64 ",\"rejected\":%" PRIu64 ",\"cpu_rejected\":%" PRIu64
        ",\"cr3_rejected\":%" PRIu64 ",\"r13_rejected\":%" PRIu64
        ",\"budget\":{\"matches\":1000000,\"seconds\":60,\"points\":32},\"points\":[",
        ctx_active ? "true" : "false", ctx_poisoned ? "true" : "false", ctx_reason,
        ctx_cr3, ctx_r13, ctx_accepted, ctx_rejected, ctx_cpu_rejected, ctx_cr3_rejected, ctx_r13_rejected);
    for (i = 0; i < ctx_npoints; i++) {
        g_string_append_printf(s, "%s\"%016" PRIx64 "\"", i ? "," : "", ctx_points[i]);
    }
    g_string_append(s, "]}"); result->state = g_string_free(s, false); return result;
}
