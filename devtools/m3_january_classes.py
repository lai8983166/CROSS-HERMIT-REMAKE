"""Choose the next school UI gesture from the live original class and standby slots."""
from devtools.m3_adventure44_orders import HANDOFF_SHA, authenticated


def party_layout(source):
    party,=authenticated(source/"formal/handoff-44.json",HANDOFF_SHA)["prepared"]["rounds"]
    result=[{"teacher":t,"slots":[-1]*4} for t in party["teacher_ids"]]
    for role,group in zip(party["student_ids"],party["student_groups"],strict=True):
        slots=result[group]["slots"]
        slots[slots.index(-1)]=role
    return result


def next_gesture(state, target):
    for kind in ("teacher","student"):
        positions={}
        for group, row in enumerate(state["classes"]):
            slots=[row["teacher"]] if kind=="teacher" else row["slots"]
            for index,role in enumerate(slots):
                if role>=0:positions[role]=("class",group,index)
        standby=state["standby_"+kind+"s"]
        for index,role in enumerate(standby):
            if role in positions:raise ValueError("Duplicated original school occupant")
            positions[role]=("standby",index)
        for group,wanted in enumerate(target):
            current=state["classes"][group]
            expected=[wanted["teacher"]] if kind=="teacher" else wanted["slots"]
            existing=[current["teacher"]] if kind=="teacher" else current["slots"]
            for index,role in enumerate(expected):
                if existing[index]==role:continue
                destination=("class",group,index)
                if role==-1:
                    return {"kind":kind,"role":existing[index],"from":destination,"to":("standby",)}
                if role not in positions:
                    raise ValueError(f"Required January {kind} {role} is unavailable")
                origin=positions[role]
                if origin[0]=="standby":
                    offset=state[kind+"_scroll"]
                    if not offset<=origin[1]<offset+5:
                        return {"kind":kind,"scroll":1 if origin[1]>=offset+5 else -1}
                return {"kind":kind,"role":role,"from":origin,"to":destination}
    return None


def screen_point(kind, location, state):
    if location[0]=="class":
        _,group,index=location
        return (50 if kind=="teacher" else 258+78*index,115+97*group)
    if len(location)==1:
        # 4A4680 returns a class member to standby when released outside all class slots.
        return 150,609 if kind=="student" else 706
    index=location[1]-state[kind+"_scroll"]
    if not 0<=index<5:raise ValueError("Requested standby portrait is not visible")
    return 155+78*index,609 if kind=="student" else 706


def gesture_input(gesture,state):
    kind=gesture["kind"]
    if "scroll" in gesture:
        # Original school control table 61B628: 15/16 and 22/23 scroll one portrait.
        return ("click",523,(606 if kind=="student" else 703)+(24 if gesture["scroll"]>0 else 0))
    return ("drag",*screen_point(kind,gesture["from"],state),*screen_point(kind,gesture["to"],state))


def main():
    import argparse
    import json
    import subprocess
    import sys
    from pathlib import Path
    from PIL import Image,ImageChops,ImageStat
    from devtools.compare_m3_native_saves import snapshot
    from devtools.isolated_windows_vm import WORKER,VMX,vmrun

    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("save",type=Path)
    parser.add_argument("sha256")
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    start=snapshot(args.save.read_bytes(),args.sha256)
    target=party_layout(args.source)
    folder=WORKER/"m3-new-baseline"
    vm=folder/VMX.name
    guest=Path("C:/ChaomofaWorker")
    if args.apply and (start["date"]!=[13,2] or start["selected_mission"]!=44):
        raise ValueError("Class changes require the original January week 2 adventure 44 school save")
    reference=folder/"school-controls.png"
    ui=folder/"host-ui.py"
    def click(*command):
        subprocess.run([sys.executable,"-B",str(ui),*map(str,command)],check=True,stdout=subprocess.DEVNULL)
    def check_school():
        click("snap")
        window=json.loads((folder/"window.json").read_bytes())
        with Image.open(folder/"screen.png") as screen,Image.open(reference) as template:
            diff=ImageChops.difference(screen.convert("RGB").crop((2,2,345,36)),template.convert("RGB"))
            if max(ImageStat.Stat(diff).mean)>=7 or window["date"]!=start["date"]:
                raise ValueError("Original school controls or date not present")
        return window["pid"]
    pid=check_school()
    vmrun(["CopyFileFromHostToGuest",vm,Path(__file__).with_name("read_m3_guest_classes.py"),guest/"m3-classes.py"],guest=True)
    def read_state():
        vmrun(["runProgramInGuest",vm,guest/"Python/python.exe",guest/"m3-classes.py",str(pid),*map(str,start["date"]),"--school-sha256",args.sha256],guest=True)
        output=folder/"live-school-classes.json"
        vmrun(["CopyFileFromGuestToHost",vm,guest/"m3-classes.json",output],guest=True)
        return json.loads(output.read_bytes())
    state=read_state()
    expected=[(g["teacher"],g["student_slots"]) for g in start["groups"]]
    if [(g["teacher"],g["slots"]) for g in state["classes"]]!=expected:
        raise ValueError("Current school groups differ from the verified departure save")
    for step in range(256):
        gesture=next_gesture(state,target)
        if gesture is None:
            print(json.dumps({"date":start["date"],"gestures":step,"classes":state["classes"]}))
            return
        action=gesture_input(gesture,state)
        if not args.apply:
            print(json.dumps({"date":start["date"],"next_gesture":gesture,"guest_input":action}))
            return
        if check_school()!=pid:raise ValueError("Original process changed")
        click(*action)
        after=read_state()
        if state==after:raise ValueError(f"Guest did not accept school gesture {step+1}: {gesture}")
        if "scroll" in gesture:
            key=gesture["kind"]+"_scroll"
            if after[key]!=state[key]+gesture["scroll"]:raise ValueError("Unexpected scroll displacement")
        elif gesture["to"][0]=="class":
            _,group,index=gesture["to"]
            occupant=after["classes"][group]
            role=occupant["teacher"] if gesture["kind"]=="teacher" else occupant["slots"][index]
            if role!=gesture["role"]:raise ValueError("Unexpected recipient of class change")
        elif gesture["role"] not in after["standby_"+gesture["kind"]+"s"]:
            raise ValueError("Returned member missing from standby")
        state=after
    raise ValueError("School arrangement exceeded the bounded gesture count")


if __name__=="__main__":
    main()
