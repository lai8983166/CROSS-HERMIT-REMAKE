"""Apply the observed timer workaround only to the stopped dedicated VM.

This is a declared compatibility profile, not a general VMware recommendation.
Cold boot + guest clock + input/graphics preflight must follow every application.
"""
import json
from devtools.isolated_windows_vm import WORKER, VMX, identity, validate_vmx, validate_disk, vmrun


def apply():
    text = VMX.read_text(encoding='utf8')
    fields = validate_vmx(text)
    validate_disk(WORKER / 'worker.vmdk')
    if str(VMX).lower() in vmrun(['list']).lower():
        raise ValueError('compatibility profile requires the stopped owned VM')
    key = 'monitor_control.virtual_rdtsc'
    if fields.get(key) == 'FALSE':
        return dict(changed=False, vmx=identity(VMX), required_preflight=True, accepted=False)
    if key in fields:
        raise ValueError('existing explicit timer profile must be reviewed, not overwritten')
    backup = WORKER / 'vmx-before-compat-profile.vmx'
    with backup.open('x', encoding='utf8') as stream:
        stream.write(text)
    updated = text.rstrip() + '\n' + key + ' = "FALSE"\n'
    validate_vmx(updated)
    VMX.write_text(updated, encoding='utf8')
    return dict(changed=True, backup=identity(backup), vmx=identity(VMX),
                host_hypervisor_changed=False, required_preflight=True, accepted=False)


if __name__ == '__main__':
    print(json.dumps(apply(), indent=2))
