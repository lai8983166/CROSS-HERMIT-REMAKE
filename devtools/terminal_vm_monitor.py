"""Bounded loopback VMware RSP control for the dedicated F-drive VM.

This is a VMM transport, not a Windows debugger. No software breakpoints,
register writes, memory writes, arbitrary monitor commands, or host UI input.
Raw readouts do not establish full state until the guest preflight verifies it.
"""
import json
import re
import socket
import subprocess
import time
from devtools.isolated_windows_vm import VMX,VMWARE,environment,validate_vmx
from devtools.vmware_rsp_state import encode_packet,decode_frame,decode_payload


def need(v,m):
    if not v:raise ValueError(m)


def endpoint():
    fields=validate_vmx(VMX.read_text(encoding='utf8'))
    need(fields.get('debugStub.listen.guest64')=='TRUE' and fields.get('debugStub.listen.guest64.remote')=='FALSE'
         and fields.get('debugStub.hideBreakpoints')=='TRUE','only hidden hardware monitor on localhost')
    literal=str(VMX).replace("'","''")
    exe=str(VMWARE/'x64/vmware-vmx.exe').replace('/','\\').replace("'","''")
    script=("$ErrorActionPreference='Stop';$rows=@(Get-NetTCPConnection -State Listen -LocalPort 8864);"
        "if(!$rows.Count){throw 'no owned monitor listener'};$result=@();foreach($row in $rows){"
        "if($row.LocalAddress -notin @('127.0.0.1','::1')){throw 'non-loopback listener'};"
        "$p=Get-CimInstance Win32_Process -Filter ('ProcessId='+$row.OwningProcess);"
        "if($p.ExecutablePath -ne '"+exe+"' -or !$p.CommandLine.Contains('"+literal+"')){throw 'wrong monitor owner'};"
        "$result+=[pscustomobject]@{address=$row.LocalAddress;port=$row.LocalPort;pid=$row.OwningProcess;exe=$p.ExecutablePath}};"
        "ConvertTo-Json -InputObject @($result) -Compress")
    p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],env=environment(),capture_output=True,text=True,timeout=20)
    need(p.returncode==0,'dedicated loopback endpoint owner must authenticate')
    return json.loads(p.stdout)


class Monitor:
    def __init__(self):
        self.owner=endpoint();self.rows=[];self.sock=None;self.stopped=False;self.breakpoints=set()
        self.sock=socket.create_connection(('127.0.0.1',8864),timeout=3);self.sock.settimeout(3)

    def receive(self,timeout=3):
        self.sock.settimeout(timeout);wire=bytearray();ack=0
        while True:
            b=self.sock.recv(1)
            if not b:raise EOFError('monitor disconnected')
            if not wire:
                if b in (b'+',b'-'):
                    need(b==b'+','monitor rejected packet checksum');ack+=1;need(ack<64,'bounded acknowledgments');continue
                need(b==b'$','RSP frame start');wire.extend(b);continue
            wire.extend(b);need(len(wire)<=131072,'bounded monitor packet')
            if b==b'#':
                for _ in range(2):
                    tail=self.sock.recv(1);need(tail,'complete checksum');wire.extend(tail)
                payload=decode_frame(bytes(wire),limit=65536);self.sock.sendall(b'+')
                self.rows.append(dict(direction='receive',monotonic=time.monotonic(),wire_hex=wire.hex(),payload_hex=payload.hex()))
                if payload[:1]in(b'T',b'S'):self.stopped=True
                return payload

    def send(self,payload):
        need(isinstance(payload,bytes)and len(payload)<8192,'bounded exact request')
        allowed=(payload in(b'?',b'g',b'qSupported',b'qfThreadInfo',b'qsThreadInfo',b'qC',b'D',b'c',b's')
            or re.fullmatch(rb'qXfer:features:read:[a-zA-Z0-9_.-]+:[0-9a-f]+,[0-9a-f]+',payload)
            or re.fullmatch(rb'(?:Hg|qThreadExtraInfo,)[0-9a-f]+',payload)
            or re.fullmatch(rb'm[0-9a-f]+,[0-9a-f]+',payload)
            or re.fullmatch(rb'[Zz]1,[0-9a-f]+,1',payload))
        if payload.startswith(b'qRcmd,'):
            command=bytes.fromhex(payload[6:].decode()).decode('ascii')
            allowed=command in ('help','r','r cr0','r cr2','r cr3','r cr4','r cs','r ss','r ds','r es','r fs','r gs','r gdtr','r idtr','r ldtr','r dr0','r dr1','r dr2','r dr3','r dr6','r dr7')
        need(allowed,'read/continue/single-step/explicit hardware breakpoint only; no write fallback')
        if payload.startswith(b'Z1,'):
            need(len(self.breakpoints)<1,'at most one VMM hardware breakpoint')
        if payload in(b'c',b's'):self.stopped=False
        self.rows.append(dict(direction='send',monotonic=time.monotonic(),payload_hex=payload.hex()))
        self.sock.sendall(encode_packet(payload))

    def query(self,payload,timeout=3):
        self.send(payload);reply=self.receive(timeout)
        if payload.startswith(b'Z1,')and reply==b'OK':self.breakpoints.add(payload[3:])
        if payload.startswith(b'z1,')and reply==b'OK':self.breakpoints.discard(payload[3:])
        return reply

    def interrupt(self):
        self.rows.append(dict(direction='interrupt',monotonic=time.monotonic()))
        self.sock.sendall(b'\x03');reply=self.receive()
        need(reply[:1]in(b'S',b'T'),'actual VM stop notification');return reply

    def monitor(self,name):
        self.send(b'qRcmd,'+name.encode().hex().encode());packets=[]
        for _ in range(64):
            p=self.receive();packets.append(p)
            if p==b'OK' or not p.startswith(b'O'):return packets
        raise ValueError('bounded monitor console output')

    def close(self):
        if self.sock is None:return
        try:
            if self.breakpoints:
                if not self.stopped:self.interrupt()
                for item in list(self.breakpoints):need(self.query(b'z1,'+item)==b'OK','remove owned hardware breakpoint')
            need(self.query(b'D')==b'OK','explicit VMM detach/resume')
            self.stopped=False
        finally:self.sock.close();self.sock=None
