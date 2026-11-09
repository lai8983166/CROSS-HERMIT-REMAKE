"""Explicit larger OFFLINE subject-record budget; original ETL is unchanged.

Every original record is still read/digested and every selected subject event
is retained. Capture limits and zero-loss/pairing requirements are unchanged.
"""
import hashlib
from pathlib import Path
from devtools import terminal_battle_wait_etl as parent
from devtools.terminal_battle_wait_etl import *
from devtools.terminal_scene_resources import clone

PARENT_SHA='3c68044529b5f5fa1b9b3426b3f12382797ab7981e51db2af2b861e935f659ce'
MAX_SELECTED=65536
SELECTED_GZIP_LIMIT=2*1024*1024
# LIMITS still authenticates the unmodified declaration in the original source.
OFFLINE_LIMITS=dict(parent.LIMITS,max_selected_records=MAX_SELECTED,
                    max_selected_gzip_bytes=SELECTED_GZIP_LIMIT)


def decode_etl(path,source,result,deadline,consume_records):
    before=hashlib.sha256(Path(parent.__file__).read_bytes()).hexdigest()
    need(before==PARENT_SHA,'fixed complete original ETL reader')
    result.update(source_declared_reader_limits=source['trace_limits'],offline_reader_limits=OFFLINE_LIMITS,
        offline_budget_expanded=True,source_rewritten=False,events_truncated=False,
        offline_budget_reason='original 16384 subject-record allocation was exhausted on the preserved battle ETL; retain complete sequence within an explicit 65536-record/2-MiB-gzip bound')
    try:
        return clone(parent.decode_etl,MAX_SELECTED=MAX_SELECTED)(path,source,result,deadline,consume_records)
    finally:
        need(hashlib.sha256(Path(parent.__file__).read_bytes()).hexdigest()==before,
             'complete original ETL reader unchanged during offline decode')
