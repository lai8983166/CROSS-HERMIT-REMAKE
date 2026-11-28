"""Observe original class slots and the current standby list order in the guest school."""
import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import struct
import sys


def groups(read):
    def values(address, fmt):
        return list(struct.unpack("<"+fmt, read(address,struct.calcsize("<"+fmt))))

    def roster(address, count_at, maximum):
        count, = values(count_at,"h")
        if not 0<=count<=maximum:
            raise ValueError("School list count out of range")
        return values(address,f"{count}h") if count else []

    classes=[]
    for group in range(5):
        at=0x7aaa12+28*group
        teacher,=values(at,"h")
        slots=values(at+16,"4h")
        count,=values(at+14,"B")
        if count!=sum(student>=0 for student in slots):
            raise ValueError("Inconsistent original class count")
        classes.append({"teacher":teacher,"slots":slots,"mode":values(at+3,"B")[0]})
    students=roster(0x7a5210,0x7a5260,40)
    teachers=roster(0x7a5262,0x7a528a,20)
    standby=roster(0x7d57e2,0x7d57de,40)
    faculty=roster(0x7d58b4,0x7d58b0,20)
    if sorted(standby+[s for c in classes for s in c["slots"] if s>=0])!=sorted(students):
        raise ValueError("Standby students and class slots do not account for the original roster")
    if sorted(faculty+[c["teacher"] for c in classes if c["teacher"]>=0])!=sorted(teachers):
        raise ValueError("Standby teachers and class slots do not account for the original faculty")
    return {"date":values(0x7a528e,"2h"),"classes":classes,"standby_students":standby,
            "standby_teachers":faculty,"student_scroll":values(0x7d57db,"B")[0],
            "teacher_scroll":values(0x7d58ac,"h")[0]}


def current_classes(pid,month,week):
    root=Path("C:/ChaomofaWorker")
    executable=root/"project/.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE"
    if hashlib.sha256(executable.read_bytes()).hexdigest()!="030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7":
        raise ValueError("Unexpected original executable")
    kernel=ctypes.windll.kernel32
    kernel.OpenProcess.restype=wintypes.HANDLE
    handle=kernel.OpenProcess(0x1010,False,pid)
    if not handle:raise ctypes.WinError()
    h=wintypes.HANDLE(handle)
    try:
        name=ctypes.create_unicode_buffer(1024)
        length=wintypes.DWORD(len(name))
        if not kernel.QueryFullProcessImageNameW(h,0,name,ctypes.byref(length)) or Path(name.value).resolve()!=executable.resolve():
            raise ValueError("Unexpected original process")
        def read(address,size):
            buf=ctypes.create_string_buffer(size)
            got=ctypes.c_size_t()
            if not kernel.ReadProcessMemory(h,ctypes.c_void_p(address),buf,size,ctypes.byref(got)) or got.value!=size:
                raise ctypes.WinError()
            return buf.raw
        state=groups(read)
        if state["date"]!=[month,week] or groups(read)!=state:
            raise ValueError("School state changed or differs from the requested date")
        return state
    finally:
        kernel.CloseHandle(h)


def main():
    root=Path("C:/ChaomofaWorker")
    sys.path.insert(0,str(root/"project"))
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pid",type=int)
    parser.add_argument("month",type=int)
    parser.add_argument("week",type=int)
    parser.add_argument("--school-sha256")
    args=parser.parse_args()
    if args.school_sha256 and hashlib.sha256((root/"m3-export.sav").read_bytes()).hexdigest()!=args.school_sha256:
        raise ValueError("Original guest export differs from the requested school save")
    state=current_classes(args.pid,args.month,args.week)
    (root/"m3-classes.json").write_text(json.dumps(state,separators=(",",":")))


if __name__=="__main__":
    main()
