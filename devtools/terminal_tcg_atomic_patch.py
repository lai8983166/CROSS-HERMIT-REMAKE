"""Create a scoped patch from the authenticated v8 tree without mutating it."""
import difflib
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'.venv-audit/native-worker/tcg-build-v1/source'
changes={}
p='target/i386/terminal-state.c';old=(S/p).read_text();changes[p]=(old,old+'\n'+(R/'devtools/terminal_tcg_atomic_checkpoint.c').read_text())
p='migration/savevm.h';old=(S/p).read_text();changes[p]=(old,old.replace('#define QEMU_VM_FILE_MAGIC','bool terminal_save_checkpoint_file(const char *filename, Error **errp);\n\n#define QEMU_VM_FILE_MAGIC',1))
p='migration/savevm.c';old=(S/p).read_text();anchor='/* Is a save state entry iterable (e.g. RAM)? */'
helper='''/* Project same-command stopped full-RAM file checkpoint. */
bool terminal_save_checkpoint_file(const char *filename, Error **errp)
{
    QIOChannelFile *ioc;
    QEMUFile *f;
    int ret, close_ret;
    if (runstate_is_running()) {
        error_setg(errp, "checkpoint requires stopped machine");
        return false;
    }
    ioc = qio_channel_file_new_path(filename, O_WRONLY | O_CREAT | O_EXCL,
                                   0600, errp);
    if (!ioc) {
        return false;
    }
    global_state_store();
    f = qemu_file_new_output(QIO_CHANNEL(ioc));
    object_unref(OBJECT(ioc));
    ret = qemu_savevm_state(f, errp);
    close_ret = qemu_fclose(f);
    if (ret >= 0 && close_ret < 0) {
        error_setg_errno(errp, -close_ret, "checkpoint close failed");
    }
    return ret >= 0 && close_ret >= 0;
}

'''
if old.count(anchor)!=1:raise ValueError('savevm anchor')
changes[p]=(old,old.replace(anchor,helper+anchor))
p='qapi/misc-i386.json';old=(S/p).read_text();changes[p]=(old,old+'''
##
# @x-save-tcg-checkpoint:
#
# Save a stopped complete stream with same-command observations.
#
# @filename: New output file; existing paths are refused.
#
# Returns: Before/after JSON for bounded project validation.
#
# Since: 11.1
##
{ 'command': 'x-save-tcg-checkpoint', 'data': { 'filename': 'str' },
  'returns': 'TcgStateJson' }
''')
out=R/'devtools/patches/terminal-tcg-atomic-checkpoint-v9.patch'
with out.open('x',newline='\n')as f:
 for p,(old,new)in changes.items():
  f.write('diff --git a/'+p+' b/'+p+'\n')
  f.writelines(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+p,tofile='b/'+p))
print(out)
