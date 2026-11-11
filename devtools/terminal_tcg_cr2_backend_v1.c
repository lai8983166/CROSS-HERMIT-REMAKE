/* Project CR2 ledger, GPL-2.0-or-later; included by terminal-state.c. */
#include "qemu/timer.h"
#define CR2_RECORDS 65536
#define CR2_BYTES (16 * 1024 * 1024)
static GMutex cr2_lock;
static bool cr2_active, cr2_poisoned, cr2_overflow;
static const char *cr2_reason = "";
static uint64_t cr2_window, cr2_seq[2], cr2_count;
static int64_t cr2_begin, cr2_elapsed;
static char *cr2_data, *cr2_start;
static size_t cr2_used;
static QEMUTimer *cr2_timer;
typedef struct CR2Pending {
    bool valid;
    uint64_t old, value, cr3, cs;
    int cpl, vector, error, access, mmu;
} CR2Pending;
static CR2Pending cr2_pending[2];

static void cr2_fail_locked(const char *reason)
{
    if (!cr2_poisoned) { cr2_reason = reason; }
    cr2_poisoned = true;
    qemu_system_vmstop_request_prepare();
    qemu_system_vmstop_request(RUN_STATE_PAUSED);
}
void terminal_cr2_poison(const char *reason)
{
    g_mutex_lock(&cr2_lock);
    if (cr2_active) { cr2_fail_locked(reason); }
    g_mutex_unlock(&cr2_lock);
}
static void cr2_expired(void *unused)
{
    terminal_cr2_poison("timeout");
}
static bool cr2_check_locked(int cpu)
{
    if (!cr2_active) { return false; }
    if (cpu < 0 || cpu > 1) { cr2_fail_locked("cpu-topology"); return false; }
    if (qemu_clock_get_ns(QEMU_CLOCK_REALTIME) - cr2_begin >= 60000000000LL) {
        cr2_fail_locked("timeout");
    }
    return !cr2_poisoned;
}
static void cr2_append_locked(CPUX86State *env, CR2Pending *p, bool pf)
{
    int cpu = env_cpu(env)->cpu_index;
    char row[1536];
    int n;
    if (!cr2_check_locked(cpu)) { return; }
    n = snprintf(row, sizeof(row),
        "%s{\"cpu\":%d,\"seq\":%" PRIu64 ",\"window\":%" PRIu64
        ",\"reason\":\"%s\",\"old\":\"%016" PRIx64 "\",\"new\":\"%016" PRIx64
        "\",\"cr3\":\"%016" PRIx64 "\",\"cs\":\"%016" PRIx64
        "\",\"cpl\":%d,\"pc\":\"%016" PRIx64 "\",\"source\":\"%016" PRIx64
        "\",\"fault_address\":\"%016" PRIx64 "\",\"vector\":%d,\"error_code\":%d,"
        "\"access_type\":%d,\"mmu_idx\":%d,\"stage2\":false,\"intercepted\":false}",
        cr2_count ? "," : "", cpu, cr2_seq[cpu] + 1, cr2_window,
        pf ? "pf" : "mov", p->old, p->value, p->cr3, p->cs, p->cpl,
        (uint64_t)(env->eip + env->segs[R_CS].base), pf ? 0 : p->value,
        pf ? p->value : 0, p->vector, p->error, p->access, p->mmu);
    if (cr2_count >= CR2_RECORDS || n < 0 || n >= sizeof(row) || cr2_used + n + 2 > CR2_BYTES) {
        cr2_overflow = true; cr2_fail_locked("overflow"); return;
    }
    memcpy(cr2_data + cr2_used, row, n); cr2_used += n;
    cr2_seq[cpu]++; cr2_count++;
}
void terminal_cr2_write(CPUX86State *env, uint64_t value, int vector,
                        int error, int access, int mmu)
{
    int cpu = env_cpu(env)->cpu_index;
    CR2Pending p;
    g_mutex_lock(&cr2_lock);
    if (cr2_check_locked(cpu)) {
        if (cr2_pending[cpu].valid) { cr2_fail_locked("pending-overlap"); }
        p = (CR2Pending){ .valid = true, .old = env->cr[2], .value = value,
            .cr3 = env->cr[3], .cs = env->segs[R_CS].selector,
            .cpl = env->hflags & HF_CPL_MASK, .vector = vector,
            .error = error, .access = access, .mmu = mmu };
        if (vector == -1) { cr2_append_locked(env, &p, false); }
        else { cr2_pending[cpu] = p; }
    }
    g_mutex_unlock(&cr2_lock);
}
void terminal_cr2_restored(CPUState *cs)
{
    int cpu = cs->cpu_index;
    g_mutex_lock(&cr2_lock);
    if (cr2_check_locked(cpu) && cr2_pending[cpu].valid) {
        CR2Pending *p = &cr2_pending[cpu];
        if (p->vector != 14 || cs->exception_index != 14 || X86_CPU(cs)->env.cr[2] != p->value) {
            cr2_fail_locked("pending-invalid");
        } else { cr2_append_locked(&X86_CPU(cs)->env, p, true); }
        p->valid = false;
    }
    g_mutex_unlock(&cr2_lock);
}
static char *cr2_boundary(Error **errp)
{
    GString *s = g_string_new("[");
    int i;
    for (i = 0; i < 2; i++) {
        TcgStateJson *v = qmp_x_query_tcg_state(i, errp);
        if (!v) { g_string_free(s, true); return NULL; }
        g_string_append_printf(s, "%s{\"cpu\":%d,\"cr2\":\"%016" PRIx64
            "\",\"counter\":%" PRIu64 ",\"state\":%s}", i ? "," : "", i,
            (uint64_t)X86_CPU(qemu_get_cpu(i))->env.cr[2], cr2_seq[i], v->state);
        qapi_free_TcgStateJson(v);
    }
    g_string_append_c(s, ']'); return g_string_free(s, false);
}
static TcgStateJson *terminal_cr2_command(int64_t command, Error **errp)
{
    CPUState *cpu;
    int n = 0, i;
    char *end = NULL, *escaped, *digest;
    TcgStateJson *result;
    if (!tcg_enabled() || runstate_is_running()) {
        error_setg(errp, "CR2 requires stopped TCG"); return NULL;
    }
    CPU_FOREACH(cpu) {
        if (!cpu->stopped || cpu->cpu_index < 0 || cpu->cpu_index > 1) {
            error_setg(errp, "CR2 requires both CPUs stopped"); return NULL;
        }
        n++;
    }
    if (n != 2) { error_setg(errp, "CR2 requires two CPUs"); return NULL; }
    if (command == -2) {
        if (cr2_active || cr2_poisoned) { error_setg(errp, "CR2 active or poisoned"); return NULL; }
        if (!cr2_data) { cr2_data = g_malloc(CR2_BYTES + 1); }
        cr2_window++; cr2_count = 0; cr2_used = 1; cr2_data[0] = '[';
        cr2_overflow = false; cr2_elapsed = 0;
        g_free(cr2_start); cr2_start = cr2_boundary(errp);
        if (!cr2_start) { return NULL; }
        cr2_begin = qemu_clock_get_ns(QEMU_CLOCK_REALTIME);
        cr2_active = true;
        if (!cr2_timer) { cr2_timer = timer_new_ns(QEMU_CLOCK_REALTIME, cr2_expired, NULL); }
        timer_mod_ns(cr2_timer, cr2_begin + 60000000000LL);
    } else {
        if (!cr2_active) { error_setg(errp, "CR2 not active"); return NULL; }
        cr2_elapsed = qemu_clock_get_ns(QEMU_CLOCK_REALTIME) - cr2_begin;
        g_mutex_lock(&cr2_lock);
        cr2_check_locked(0);
        for (i = 0; i < 2; i++) {
            if (cr2_pending[i].valid) { cr2_fail_locked("pending-at-end"); }
        }
        g_mutex_unlock(&cr2_lock);
        end = cr2_boundary(errp); if (!end) { return NULL; }
        cr2_active = false; timer_del(cr2_timer);
    }
    cr2_data[cr2_used] = ']'; cr2_data[cr2_used + 1] = 0;
    digest = g_compute_checksum_for_data(G_CHECKSUM_SHA256, (guchar *)cr2_data, cr2_used + 1);
    /* g_strescape emits only JSON-compatible escapes for this ASCII event stream. */
    escaped = g_strescape(cr2_data, NULL);
    result = g_new0(TcgStateJson, 1);
    result->state = g_strdup_printf("{\"schema\":\"tcg-cr2-ledger-v1\",\"phase\":\"%s\","
        "\"window\":%" PRIu64 ",\"poisoned\":%s,\"poison_reason\":\"%s\",\"overflow\":%s,"
        "\"count\":%" PRIu64 ",\"bytes\":%zu,\"elapsed_ns\":%" PRId64 ","
        "\"budget\":{\"records\":65536,\"bytes\":16777216,\"seconds\":60},"
        "\"start\":%s,\"end\":%s,\"events_json\":\"%s\",\"events_sha256\":\"%s\"}",
        command == -2 ? "arm" : "end", cr2_window, cr2_poisoned ? "true" : "false",
        cr2_reason, cr2_overflow ? "true" : "false", cr2_count, cr2_used + 1,
        cr2_elapsed, cr2_start, end ? end : "[]", escaped, digest);
    g_free(end); g_free(escaped); g_free(digest); return result;
}
