"""Add exact read-only p-register requests to the frozen VMM transport."""
import re,time
from devtools import terminal_vm_monitor_v2 as parent
from devtools.vmware_rsp_state import encode_packet


class Monitor(parent.Monitor):
    def send(self,payload):
        if re.fullmatch(rb'p[0-9a-f]+',payload)and int(payload[1:],16)<=56:
            self.rows.append(dict(direction='send',monotonic=time.monotonic(),payload_hex=payload.hex()))
            self.sock.sendall(encode_packet(payload));return
        super().send(payload)
