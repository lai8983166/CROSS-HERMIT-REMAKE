"""Original native prefix validation under the honestly identified new device build.

The leaf verifiers are unchanged; no previous build metadata or trace is fabricated.
"""
from tools.school_font_finish_verification import parent,verify_finish,OWNER,TOP,COUNTER,BASE,SECOND,SIZE,dword,store
from tools.school_font_finish import PHASES as FONT_PHASES


def verify_native_prefix(c):
    owner,image,objects=parent.verify_prefix(c);objects=parent.verify_atlas(c,owner,image,objects);parent.verify_gdi(c,owner,image)
    dib=parent.verify_raster(c,owner,image);parent.verify_pixels(c,owner,image,objects,dib)
    for p in ('cleanup','vertex','states'):objects=parent.verify_phase(c,p,owner,image,objects)
    for p in ('loop','constructor','atlas'):parent.verify_second(c,p,owner,image,objects)
    owner=bytearray(owner);store(owner,0x1094,SECOND);image=bytearray(image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+SIZE)
    for p in ('texture','gdi'):objects=parent.verify_resource(c,p,bytes(owner),bytes(image),objects)
    parent.verify_retirement(c,bytes(owner),bytes(image));dib=parent.verify_second_raster(c,bytes(owner),bytes(image));parent.verify_second_upload(c,bytes(owner),bytes(image),objects,dib)
    for p in FONT_PHASES:objects=verify_finish(c,p,bytes(owner),bytes(image),objects)
    dc=dict(second_font_state_block_delete_results=[0,0],font_state_block_delete_results=[0,0],second_font_texture_unbind_hr=0,second_font_vertex_buffer_release_count=0,
        font_texture_unbind_hr=0,font_vertex_buffer_release_count=0,second_atlas_texture_release_count=0,atlas_texture_release_count=0,
        texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
    pc=dict(second_atlas_fonts_released=0,second_atlas_dcs_released=0,second_atlas_bitmaps_released=0,second_atlas_selection_restored=True,
        second_native_GDI_cleanup_executed=True,second_native_atlas_fonts_released=1,second_native_atlas_dcs_released=1,second_native_atlas_bitmaps_released=1,second_native_bitmap_delete_issued=True,
        native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,native_bitmap_delete_issued=True,native_cleanup_completed=True,
        atlas_fonts_released=0,atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
    d=parent.device_calls(c)+c['pixel_upload']['api_calls']+c['font_vertex']['api_calls']+c['font_states']['api_calls']+c['second_atlas']['api_calls']+c['second_texture']['api_calls']+c['second_upload']['api_calls']+c['finish_vertex']['api_calls']+c['finish_states']['api_calls']
    p=parent.platform_calls(c)+c['font_cleanup']['api_calls']+c['second_GDI']['api_calls']+c['second_raster']['inspections'][:1]+c['second_raster']['api_calls']+c['second_raster']['inspections'][1:]+c['finish_cleanup']['api_calls']
    return objects,dc,pc,d,p
