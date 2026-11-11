"""Bounded buffered QMP framing for a maximum 16 MiB event array."""
import json
import socket


class QMP:
    LIMIT = 64 * 1024 * 1024

    def __init__(self, path):
        self.s = socket.socket(socket.AF_UNIX)
        self.s.settimeout(10)
        self.s.connect('\0' + str(path))
        self.f = self.s.makefile('rwb', buffering=64 * 1024)
        self.receipts = []
        self.greeting = self.read()
        self.call('qmp_capabilities')

    def read(self):
        raw = self.f.readline(self.LIMIT + 1)
        if not raw.endswith(b'\n') or len(raw) > self.LIMIT:
            raise ValueError('QMP EOF or frame budget')
        return json.loads(raw)

    def call(self, name, args=None):
        request = dict(execute=name, id=len(self.receipts) + 1)
        if args is not None:
            request['arguments'] = args
        self.f.write(json.dumps(request).encode() + b'\n')
        self.f.flush()
        for _ in range(128):
            response = self.read()
            if response.get('id') == request['id']:
                self.receipts.append(dict(request=request, response=response))
                return response
        raise ValueError('QMP unsolicited message budget')
