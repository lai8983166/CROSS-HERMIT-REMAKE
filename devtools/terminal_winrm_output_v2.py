"""Durable per-command WinRM output; a lost Receive reply remains unknown.

Single receiver only. Never replay a command or a Send request here.
"""
import base64
import json
import os
import re
from pathlib import Path


def receive(protocol, directory, shell, command):
    from winrm.exceptions import WinRMOperationTimeoutError
    if any(not re.fullmatch(r'[A-Fa-f0-9-]{36}', x) for x in (shell, command)):
        raise ValueError('owned command IDs required')
    directory = Path(directory)
    prefix = 'receive-' + command.lower() + '-'
    pending = directory / (prefix + 'pending')
    if pending.exists():
        raise ValueError('Receive outcome unknown; read guest durable result instead')
    stdout, stderr, count = [], [], 0
    for path in sorted(directory.glob(prefix + '*.json')):
        if path.name != prefix + f'{count:06d}.json':
            raise ValueError('non-contiguous receipt')
        row = json.loads(path.read_bytes())
        if row['shell'] != shell or row['command'] != command:
            raise ValueError('receipt owner mismatch')
        stdout.append(base64.b64decode(row['stdout'], validate=True))
        stderr.append(base64.b64decode(row['stderr'], validate=True))
        count += 1
        if row['done']:
            return b''.join(stdout), b''.join(stderr), row['code']
    while True:
        with pending.open('x', encoding='utf8') as stream:
            json.dump(dict(shell=shell, command=command, index=count), stream)
            stream.flush(); os.fsync(stream.fileno())
        try:
            out, err, code, done = protocol.get_command_output_raw(shell, command)
        except WinRMOperationTimeoutError:
            pending.unlink()
            continue
        row = dict(shell=shell, command=command, stdout=base64.b64encode(out).decode(),
                   stderr=base64.b64encode(err).decode(), code=code, done=done)
        path = directory / (prefix + f'{count:06d}.json')
        # Flush before another blocking call. A partial receipt fails closed on resume.
        with path.open('x', encoding='utf8') as stream:
            json.dump(row, stream); stream.flush(); os.fsync(stream.fileno())
        pending.unlink()
        count += 1
        stdout.append(out); stderr.append(err)
        if done:
            return b''.join(stdout), b''.join(stderr), code
