"""Bound host execution slices before recording an original instruction."""
SLICE_INSTRUCTIONS=1_000_000

def yield_before_observation(uc,point,stop,current,first,limit=SLICE_INSTRUCTIONS):
 if point!=stop and current-first>=limit:
  uc.emu_stop()
  return True
 return False
