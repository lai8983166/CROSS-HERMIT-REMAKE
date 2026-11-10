"""Explicit KD continuation state; historical prompts never authorize commands.

This is an owned-fixture development observer, not a full-state provider.
"""
import re
import time
from devtools.terminal_kd_session import need,at_prompt,pending_debug_break
from devtools.terminal_kd_session_v2 import Session as Prior


def marker_complete(tail,marker):
    return bool(re.search(r'(?:^|\n|[0-9]+: kd> )'+re.escape(marker)+r'\r?$',tail,re.M)) and at_prompt(tail)


class Session(Prior):
    def __init__(self,log,*,break_on_connect=True):
        super().__init__(log,break_on_connect=break_on_connect)
        self.state='connecting';self.transitions=[];self.stopped_text='';self.seen_length=0

    def transition(self,state,reason):
        self.state=state
        self.transitions.append(dict(state=state,reason=reason,seconds=time.monotonic(),characters=len(self.text())))

    def observe_prompt(self):
        text=self.text();tail=text[self.cursor:]
        if len(text)!=self.seen_length:
            self.transitions.append(dict(state=self.state,reason='output grew',seconds=time.monotonic(),characters=len(text)))
            self.seen_length=len(text)
        if self.state in ('connecting','running') and tail.strip() and at_prompt(tail):
            self.stopped_text=tail;self.transition('stopped','fresh prompt after cursor')
        return self.state=='stopped'

    def wait_prompt(self,seconds=10):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if self.observe_prompt():return self.stopped_text
            need(self.process.poll() is None,'SDK client exited')
            time.sleep(.02)
        raise TimeoutError('bounded fresh debugger prompt')

    def execute(self,command):
        allowed=command in ('lm m nt','r','bc *','bl','.lastevent','r dr0,dr1,dr2,dr3,dr6,dr7','r cr0,cr2,cr3,cr4')
        allowed |= bool(re.fullmatch(r'!process [0-9a-f]+ 2',command))
        allowed |= bool(re.fullmatch(r'(?:dq|db|u) [0-9a-f`]+ L[0-9a-f]{1,3}',command))
        allowed |= bool(re.fullmatch(r'\? @\$(?:tpid|tid|thread|proc|pcr)',command))
        allowed |= bool(re.fullmatch(r'ba e 1 /p ffff[0-9a-f`]+ /t ffff[0-9a-f`]+ ffff[0-9a-f`]+',command))
        need(allowed,'read-only query or owned scoped hardware breakpoint')
        need(self.observe_prompt(),'query requires confirmed current stop')
        self.sequence+=1;marker='OWNED_QUERY_END_'+str(self.sequence)
        start=len(self.text());self.transition('query','explicit query');self.send(command+';.echo '+marker)
        end=time.monotonic()+10
        while time.monotonic()<end:
            text=self.text();tail=text[start:]
            if marker_complete(tail,marker):
                self.cursor=len(text);self.stopped_text=tail;self.transition('stopped','query completed')
                need(not re.search(r'(?i)(syntax error|numeric expression missing|could not resolve|unable to insert)',tail),'debugger command refused')
                return tail
            need(self.process.poll() is None,'SDK exited during query');time.sleep(.02)
        self.transition('unknown','query timed out')
        raise TimeoutError('bounded debugger query')

    def go(self):
        need(self.observe_prompt(),'continue requires confirmed current stop')
        self.cursor=len(self.text());self.stopped_text='';self.transition('running','explicit g');self.send('g')

    def poll_stop(self):
        if not self.observe_prompt():return None
        tail=self.stopped_text
        if pending_debug_break(tail):
            need(self.pending_breaks<4,'bounded pending debugger breaks')
            event=self.execute('.lastevent');need('80000003' in event,'only explicit debugger-created break')
            self.pending_breaks+=1;self.go();return None
        return tail

    def close_after_resume(self):
        need(self.state=='running' and not self.observe_prompt(),'close requires continued guest and no new stop')
        self.process.terminate();self.process.wait(timeout=5);self.file.close();self.transition('closed','guest response already checked by caller')
