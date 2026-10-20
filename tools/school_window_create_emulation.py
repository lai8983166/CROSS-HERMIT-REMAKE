"""Reuse original callback executor with admission through real WM_CREATE."""
import argparse
import json
from tools.school_window_create import *
from tools.school_window_callback_emulation import CallbackEmulator,REGISTERS,initial_cpu,buffer_evidence
from tools.school_window_create_platform import CreatePlatform,CallbackBoundary


class CreateEmulator(CallbackEmulator):
    def __init__(self,p,fill):
        super().__init__(p,fill);self.completed_create=False

    def callback(self,packet):
        if self.completed_create:
            self.pending_callback=self.prepare_callback(packet)
            raise CallbackBoundary(packet,STOP_REASON)
        index=len(self.completed_callbacks)
        if index>=len(MESSAGES) or packet['message']!=MESSAGES[index]:raise CallbackBoundary(packet,'unadmitted client/create callback order')
        if packet['message']==131:
            if packet['data_kind']!='RECT':raise CallbackBoundary(packet,'unadmitted WM_NCCALCSIZE form')
            rectangle(bytes.fromhex(packet['data_hex']),packet['wParam'])
        if packet['message']==1:
            data=bytes.fromhex(packet['data_hex'])
            if packet['data_kind']!='CREATESTRUCTA' or len(data)!=48 or dword(data,0)!=parent.OWNER or dword(data,4)!=self.module:
                raise ValueError('actual ordinary creation owner/module/struct')
        # Parent executes the same untouched original code. Its previous admission
        # policy stopped after129; only that orchestration gate is extended here.
        self.completed_nc=False
        result=super().callback(packet)
        self.completed_nc=True
        if packet['message']==1:self.completed_create=True
        return result

    def enter_creation(self,prior):
        super().enter_creation(prior)
        if not self.completed_create or [n['setup']['packet']['message'] for n in self.completed_callbacks]!=list(MESSAGES):
            raise ValueError('real WM_CREATE completion required')


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with CreatePlatform() as p:
            e=CreateEmulator(p,fill);c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu(),module_input=e.module_input)
            prior=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,prior);prior=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,prior);prior=c[phase]
            for phase in geometry.STOPS:c[phase]=e.resume_geometry(phase,prior);prior=c[phase]
            for phase in callback.previous.module.STOPS:c[phase]=e.resume_resources(phase,prior);prior=c[phase]
            for phase in callback.previous.STOPS:c[phase]=e.resume_class(phase,prior);prior=c[phase]
            e.enter_creation(prior)
            c.update(creation=e.creation,callbacks=e.completed_callbacks,pending_callback=e.pending_callback,
                final_guarded_owner=buffer_evidence(e.bytes(parent.OWNER-4096,parent.BACKING+8192)),final_image_sha256=hashlib.sha256(e.bytes(BASE,len(e.image))).hexdigest(),
                platform_trace=p.trace,wire=p.wire,platform_abort=p.abort_proof,platform_cleanup=p.cleanup)
        cases.append(c);print(hex(fill)+': actual original callbacks '+str([n['setup']['packet']['message'] for n in c['callbacks']])+'; unanswered next '+str(c['pending_callback']['packet']['message']),flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-window-create-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        one_original_CPU_per_case=True,original_callback_executed=True,WM_NCCREATE_completed=True,WM_NCCALCSIZE_completed=True,WM_CREATE_completed=True,
        CreateWindowExA_return_received=False,HWND_global_published=False,original_IAT_modified=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable client/create trajectory required')
    out.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
