"""Second original glyph/upload ABI and explicit deleted-DIB shadow retirement."""
import argparse
import json
from copy import deepcopy
from functools import lru_cache
from tools.school_font_glyph import (ROOT,SOURCE,SOURCE_SHA256,BASE,SIZE,RANGES,IMPORTS,
    layout,glyph_object,pixels,source_contract as glyph_source,Cs,CS_ARCH_X86,CS_MODE_32)
from tools.school_font_second_resource import SECOND,source_contract as resource_source


def retire_regions(regions):
    if len(regions)!=2 or [r.get('name') for r in regions]!=['DIB','texture']:
        raise ValueError('second glyph exact first DIB/texture shadow set')
    for r in regions:
        if not 0<r['pointer']<=0xFFFFFFFF or r['data_bytes']<=0:
            raise ValueError('second glyph actual bounded retired resource identity')
        start=(r['pointer']&~4095)-4096
        end=((r['pointer']+r['data_bytes']+4095)&~4095)+4096
        if r['base']!=start or r['bytes']!=end-start or start<0 or end>0x100000000:
            raise ValueError('second glyph exact guarded retirement mapping')
    a,b=regions
    if a['data_bytes']!=262144 or a['base']<b['base']+b['bytes'] and b['base']<a['base']+a['bytes']:
        raise ValueError('second glyph deleted DIB must not overlap live texture')
    return [deepcopy(b)],[dict(region=deepcopy(a),reason='first DIB released by verified original GDI sequence',
        audit_mapping_unmapped=True,host_release_performed_by_retirement=False,native_game_call_executed=False)]


@lru_cache(maxsize=1)
def source_contract():
    return dict(shared_glyph_source=glyph_source(),second_resource_source=resource_source(),
        second_object=SECOND,characters=list(range(32,127)),UV_offset=112,UV_bytes=1520,
        retired_region_name='DIB',retirement_requires_original_first_GDI_deletion=True,
        retirement_preserves_CPU=True,retirement_is_audit_mapping_only=True,
        first_texture_shadow_must_remain=True,first_texture_actual_readback_after_second_upload=True,
        raster_stop='0x401660',upload_stop='0x4017b6',original_cleanup_executed=False,
        full415F50_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable second glyph source required')
    path.write_text(json.dumps(source_contract(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
