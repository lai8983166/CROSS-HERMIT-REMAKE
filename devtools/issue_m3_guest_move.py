"""Select an original student and compare the queued click with its requested cell or target."""
import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import sys
import time


def main():
    root=Path("C:/ChaomofaWorker")
    sys.path[:0]=[str(root),str(root/"project")]
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    from read_m3_guest_battle import observe
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("pid","scene","month","week","slot","role","x","y"):
        parser.add_argument(name,type=int)
    parser.add_argument("save_sha256")
    parser.add_argument("--target-slot",type=int,help="right-click this specific active original unit")
    args=parser.parse_args()
    dimensions={18:(64,96),44:(96,144)}
    width,height=dimensions[args.scene]
    if not (0<=args.x<width and 0<=args.y<height):
        raise ValueError("Requested destination outside original terrain")
    if hashlib.sha256((root/"m3-export.sav").read_bytes()).hexdigest()!=args.save_sha256:
        raise ValueError("Original departure save differs")
    game=root/"project/.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE"
    def state():
        snapshot=observe(args.pid,args.scene,game,True)
        if snapshot["date"]!=[args.month,args.week]:raise ValueError("Unexpected tactical date")
        unit=next(u for u in snapshot["units"] if u["slot"]==args.slot)
        if (unit["role"],unit["side"],unit["state"])!=(args.role,0,1):
            raise ValueError("Requested student is unavailable")
        return snapshot
    user=ctypes.windll.user32
    user.SetProcessDPIAware()
    def focus():
        hwnd=user.GetForegroundWindow()
        pid=wintypes.DWORD()
        user.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
        rect=wintypes.RECT()
        if (pid.value!=args.pid or not user.GetWindowRect(hwnd,ctypes.byref(rect))
                or (rect.left,rect.top,rect.right,rect.bottom)!=(0,0,1024,768)):
            raise ValueError("Original game lost guest focus or viewport size changed")
    def click(point,right=False):
        focus()
        if not (0<=point[0]<1024 and 0<=point[1]<768):raise ValueError("Point outside guest viewport")
        user.SetCursorPos(*point)
        time.sleep(.06)
        focus()
        user.mouse_event(8 if right else 2,0,0,0,0)
        try:time.sleep(.10)
        finally:user.mouse_event(16 if right else 4,0,0,0,0)
        time.sleep(.12)
    def selected(snapshot):
        return [r["slot"] for r in snapshot["command_state"] if r["selected"]]
    def center(cell):
        click((797+int((cell[0]+.5)*170/width),616+int((cell[1]+.5)*128/height)))
        time.sleep(.35)
    before=state()
    student=next(r for r in before["units"] if r["slot"]==args.slot)
    center(student["cell"])
    view=state()
    point=next(r["screen"] for r in view["screen_positions"] if r["slot"]==args.slot)
    if not (60<=point[0]<964 and 30<point[1]<600):
        raise ValueError("Student outside map viewport after centering")
    if selected(view)!=[args.slot]:
        focus()
        user.SetCursorPos(*point)
        time.sleep(.12)
        if state()["cursor"]["target"]!=args.slot:raise ValueError("Original hover did not identify the requested student")
        click(point)
    chosen=state()
    if selected(chosen)!=[args.slot]:raise ValueError(f"Student selection differs: {selected(chosen)}")
    destination=[args.x,args.y]
    if args.target_slot is not None:
        target=next((u for u in chosen["units"] if u["slot"]==args.target_slot and u["state"]==1),None)
        if not target:raise ValueError("Original target unavailable")
        destination=target["cell"]
    center(destination)
    moved=state()
    if selected(moved)!=[args.slot]:raise ValueError("Selection changed before order")
    camera=moved["camera"]
    point=(destination[0]*32+16-camera[0],destination[1]*16+8-camera[1]+30)
    if args.target_slot is not None:
        centers=moved["screen_positions"]
        target=next((row for row in centers if row["slot"]==args.target_slot),None)
        if not target:raise ValueError("Original target disappeared")
        point=target["screen"]
        destination=next(u["cell"] for u in moved["units"] if u["slot"]==args.target_slot)
    if not (60<=point[0]<964 and 30<point[1]<600):
        raise ValueError("Destination outside map viewport after centering")
    offsets=[(0,0)]
    if args.target_slot is not None:
        rw,rh=target["hit_radius"]
        offsets.extend([(0,-rh//2),(-rw//2,0),(rw//2,0),(0,rh//2)])
    for dx,dy in offsets:
        pixel=(point[0]+dx,point[1]+dy)
        if not (60<=pixel[0]<964 and 30<pixel[1]<600):continue
        focus()
        user.SetCursorPos(*pixel)
        time.sleep(.12)
        hovered=state()
        cursor=hovered["cursor"]
        mouse=wintypes.POINT()
        if not user.GetCursorPos(ctypes.byref(mouse)):raise ctypes.WinError()
        world=[mouse.x+hovered["camera"][0],mouse.y-30+hovered["camera"][1]]
        if args.target_slot is not None:
            matches=cursor["target"]==args.target_slot
        else:
            matches=cursor["target"]==-1 and [world[0]//32,world[1]//16]==destination
        if matches:
            point=pixel
            break
    else:raise ValueError(f"Original hover did not resolve requested destination {destination}")
    click(point,True)
    after=state()
    receipt={"scene":args.scene,"date":after["date"],"departure_sha256":args.save_sha256,
             "actor_slot":args.slot,"role":args.role,"target_cell":destination,"target_slot":args.target_slot,"screen":point,
             "cursor_before_order":cursor,"selected_at":chosen["elapsed"],"before_click":moved["elapsed"],"after_click":after["elapsed"],
             "before":next(r for r in moved["command_state"] if r["slot"]==args.slot),
             "after":next(r for r in after["command_state"] if r["slot"]==args.slot)}
    packet=receipt["after"]["first_pending_command"]
    receipt["order_evidence"]="unobserved"
    if packet and packet!=receipt["before"]["first_pending_command"]:
        data=bytes.fromhex(packet)
        if args.target_slot is None:
            matches=data[0]==1 and data[1]==args.slot and list(data[3:5])==destination
        else:
            matches=data[0] in (2,3) and data[1]==args.slot and data[2]==args.target_slot
        receipt["order_evidence"]="matching_pending_order" if matches else "different_pending_order"
    if args.target_slot is None:
        expected_goal=[destination[0]*32+16,destination[1]*16+8]
        receipt["requested_goal_observed"]=(receipt["after"]["goal_pixels"]==expected_goal
                                           and receipt["before"]["goal_pixels"]!=expected_goal)
    else:
        receipt["requested_target_observed"]=(receipt["after"]["target_id"]==args.target_slot
                                             and receipt["before"]["target_id"]!=args.target_slot)
    (root/"m3-move-receipt.json").write_text(json.dumps(receipt,separators=(",",":")))


if __name__=="__main__":
    try:
        main()
    except Exception as error:
        root=Path("C:/ChaomofaWorker")
        if (root/"isolation-qualified.json").is_file():
            (root/"m3-move-error.txt").write_text(str(error))
        raise
