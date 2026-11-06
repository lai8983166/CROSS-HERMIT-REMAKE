"""Derive GPU namespaces from current original calls, VM PC and record owners."""
import struct

from tools import terminal_unit_frontends_emulation as source
from tools import terminal_followup_emulation as followup
from tools import terminal_replacement_emulation as replacement
from tools import terminal_next_dialogue_emulation as next_dialogue
from tools import terminal_multiline_emulation as multiline
from tools import terminal_last_dialogue_emulation as last_dialogue
from tools import terminal_unit_frontends_minimap as minimap
from tools.terminal_unit_frontends_platform_verification import PlatformVerifier,need,word

POINTER='overlay-followup-text-pointer'
BITS='overlay-followup-text-bits'


def get(replay,p):
    return word(replay.read(p,4))


class Projection:
    def __init__(self,case):
        self.case=case
        self.bridge=None
        self.resource_stack=[]
        self.unit=None
        self.image=None
        self.expected='overlay'
        self.approved={}
        self.last_namespace_started=False
        self.retired=[]
        self.replay=None
        self.slot=None

    def observe(self,replay,pc):
        if replay.budget_stop:return
        check=(pc in (0x466C80,0x466D85,0x41F340,0x416790) or
               self.resource_stack and pc==self.resource_stack[-1]['return'][0])
        cpu=replay.cpu() if check else None
        if cpu is None:return
        sp=cpu['ESP']
        while self.resource_stack and (pc,sp)==self.resource_stack[-1]['return']:
            self.resource_stack.pop();self.image=None
        if pc==0x466C80:
            ordinal=get(replay,source.previous.CTRL+0x2E6F0)
            need(ordinal in (0,1) and self.unit is None,'two natural original cache load contexts')
            need(get(replay,sp+4)==source.previous.CTRL+0x2A6F0+ordinal*8,
                 'current original cache entry determines unit identity namespace')
            self.unit=ordinal
        elif pc==0x466D85:
            need(self.unit is not None,'original unit loader returns from active cache context')
            self.unit=None;self.image=None
        elif pc==0x416790 and self.unit is None:
            group=get(replay,sp+8)
            need(group in (20,30,31,32,90),'only declared overlay, portrait and COMMON image registration groups')
            self.resource_stack.append(dict(group=group,return_ESP=sp,
                                            **{'return':(get(replay,sp),sp+12)}))
        elif pc==0x41F340:
            index=get(replay,sp+12);base=get(replay,sp+16)
            need(index<580,'bounded original image loader index')
            domain=('overlay-unit-frontends-'+str(self.unit)+'-'+str(index) if self.unit is not None
                    else 'overlay-battle-exit-common-'+str(index)
                    if self.resource_stack and self.resource_stack[-1]['group']==90 else None)
            self.image=dict(record=base+index*84,domain=domain)

    def domain(self,replay,record):
        if record in (minimap.BACKGROUND,minimap.FOG):
            return minimap.DOMAINS[0 if record==minimap.BACKGROUND else 1]
        if self.image is not None and self.image['record']==record and self.image['domain']:
            return self.image['domain']
        pc=get(replay,source.previous.VM+28)
        name=self.case['name']
        if name=='timeout_before_combat' and pc==180 and record==followup.OLD_TEXT_RECORD:
            return POINTER
        branch=replacement.branch(name)
        for i,at in enumerate(branch['text_PCs']):
            if pc==at:
                need(record==replacement.TEXTURE+i*replacement.STRIDE,
                     'replacement namespace derives from actual layer7 record and opcode PC')
                return 'overlay-replacement-'+str(i)
        branch=next_dialogue.branch(name)
        if branch['first_PC']<=pc<branch['final_PC']:
            if record==followup.NAME_RECORD:return 'overlay-next-dialogue-name'
            portrait=get(replay,source.previous.MAIN+0x844+30*8)
            if portrait and record==portrait:return 'overlay-next-dialogue-portrait'
            need(pc==branch['text_PC'] and record==branch['object']+0x28,
                 'next dialogue namespace derives from current original record and opcode PC')
            return 'overlay-next-dialogue-text'
        for module,prefix in ((multiline,'overlay-multiline-'),(last_dialogue,'overlay-last-dialogue-')):
            for i,line in enumerate(module.branch(name)['lines']):
                if pc==line['PC']:
                    need(record==module.record_at(line['layer'],line['record_index']),
                         'new multiline namespace derives from actual original layer/index')
                    return prefix+str(i)
        return 'overlay'

    def approve(self,domain,native,guest):
        key=domain,native
        if key in self.approved:return self.approved[key]==guest
        if domain in minimap.DOMAINS:
            if domain!=self.expected:return False
            count=sum(d==domain for d,p in self.bridge.used_projection)
            base=0x3C000000+minimap.DOMAINS.index(domain)*0x100000
            expected=base+(0x20000 if self.slot==64 else (count+1)*4096)
            if guest!=expected:return False
        elif domain==BITS:
            if self.expected!=POINTER:return False
            retired=[t for t in self.retired if t['record']==followup.OLD_TEXT_RECORD
                     and t.get('width')==128 and t.get('height')==32 and t.get('pitch')==256
                     and t.get('length')==8192 and t['domain']=='overlay']
            need(retired,'original prior 128x32 layer5 surface actually released before alias reuse')
            if guest!=retired[-1]['bits']:return False
        else:
            if domain!=self.expected:return False
            known=(domain in (POINTER,'overlay-next-dialogue-name','overlay-next-dialogue-portrait',
                              'overlay-next-dialogue-text') or
                   domain in tuple('overlay-replacement-'+str(i) for i in range(2)) or
                   domain in tuple('overlay-multiline-'+str(i) for i in range(3)) or
                   domain in tuple('overlay-last-dialogue-'+str(i) for i in range(3)))
            if not known:return False
            if domain.startswith('overlay-last-dialogue-') and not self.last_namespace_started:
                need(self.replay is not None and all(b<0x48001000 or a>=0x49501000
                     for a,b,_ in self.replay.u.mem_regions()),'complete new last-dialogue namespace disjoint before mapping')
                self.bridge.overlay_next=0x48001000
                self.last_namespace_started=True
            if guest!=self.bridge.overlay_next:return False
            self.bridge.overlay_next+=0x100000
        self.approved[key]=guest
        return True


class HistoricalPlatformVerifier(PlatformVerifier):
    def __init__(self,row,code,files):
        self.policy=Projection(row['input'])
        super().__init__(row,code,files,self.policy.approve)
        self.policy.bridge=self

    def identity(self,domain,native,slots):
        if domain!=POINTER:return super().identity(domain,native,slots)
        need(set(native)=={'pointer','vtable','methods'} and set(native['methods'])=={str(s) for s in slots},
             'complete mixed-domain original followup texture identity')
        return dict(pointer=self.project(POINTER,native['pointer']),
                    vtable=self.project('overlay',native['vtable']),
                    methods={str(s):self.project('overlay',native['methods'][str(s)]) for s in sorted(slots)})

    def surface(self,domain,native,size):
        if domain==POINTER:
            need(size==8192,'only explicit retired 128x32 surface alias')
            domain=BITS
        return super().surface(domain,native,size)

    def gpu(self,replay,slot,pc,effects):
        self.policy.replay=replay
        self.policy.slot=slot
        sp=replay.cpu()['ESP']
        projections=self.projections
        retired=None
        if slot==80:
            record=get(replay,sp+32)-44
            self.policy.expected=self.policy.domain(replay,record)
            q=self.traces['GPU'][self.cursor['GPU']]['reply']['result']
            native=q['texture']['pointer']
            # Filter possible reused native generations by independent current
            # original context, before the base checker selects an identity.
            self.projections={key:value for key,value in projections.items()
                              if key[1]!=native or key[0]==self.policy.expected}
        else:
            texture=self.textures.get(get(replay,sp+4))
            need(texture is not None,'current owned GPU generation')
            self.policy.expected=texture['domain']
            if slot==8:retired=dict(texture)
        try:
            result=super().gpu(replay,slot,pc,effects)
        finally:
            self.projections=projections
        if retired is not None:self.policy.retired.append(retired)
        return result
