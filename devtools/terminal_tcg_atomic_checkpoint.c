/* Project bounded synchronous checkpoint and same-command observations.
 * GPL-2.0-or-later. No injected guest register, RAM or IRQ values.
 */
#include "migration/savevm.h"
#include "system/bql.h"

static char *terminal_capture_checkpoint(Error **errp)
{
    TcgStateJson *observation, *cpu;
    CPUState *cs;
    GString *s;
    int i = 0;
    observation = qmp_x_query_tcg_checkpoint(errp);
    if (!observation) {
        return NULL;
    }
    s = g_string_new("{\"observation\":");
    g_string_append(s, observation->state);
    qapi_free_TcgStateJson(observation);
    g_string_append(s, ",\"states\":[");
    CPU_FOREACH(cs) {
        cpu = qmp_x_query_tcg_state(cs->cpu_index, errp);
        if (!cpu) {
            g_string_free(s, true);
            return NULL;
        }
        if (i++) { g_string_append_c(s, ','); }
        g_string_append(s, cpu->state);
        qapi_free_TcgStateJson(cpu);
    }
    g_string_append(s, "]}");
    return g_string_free(s, false);
}

TcgStateJson *qmp_x_save_tcg_checkpoint(const char *filename, Error **errp)
{
    g_autofree char *before = NULL;
    g_autofree char *after = NULL;
    TcgStateJson *result;
    if (!bql_locked()) {
        error_setg(errp, "checkpoint requires BQL");
        return NULL;
    }
    before = terminal_capture_checkpoint(errp);
    if (!before || !terminal_save_checkpoint_file(filename, errp)) {
        return NULL;
    }
    after = terminal_capture_checkpoint(errp);
    if (!after) {
        return NULL;
    }
    result = g_new0(TcgStateJson, 1);
    result->state = g_strdup_printf("{\"before\":%s,\"after\":%s}",
                                    before, after);
    return result;
}
