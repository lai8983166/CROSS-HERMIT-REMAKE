
void FUN_0056f420(void *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  int *_Dst;
  
  if ((((DAT_007619c0 & 4) != 0) && (iVar2 = FUN_0056fb70(), iVar2 == 0)) &&
     (iVar2 = FUN_00573780(2,"dbgheap.c",0x402,0,"_CrtCheckMemory()"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (param_1 != (void *)0x0) {
    iVar2 = (*(code *)PTR_FUN_00762130)(3,param_1,0,param_2,0,0,0);
    if (iVar2 == 0) {
      iVar2 = FUN_00573780(0,0,0,0,&DAT_00592a18,"Client hook free failure.\n");
      if (iVar2 == 1) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    else {
      iVar2 = FUN_00570050(param_1);
      if ((iVar2 == 0) &&
         (iVar2 = FUN_00573780(2,"dbgheap.c",0x414,0,"_CrtIsValidHeapPointer(pUserData)"),
         iVar2 == 1)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      _Dst = (int *)((int)param_1 + -0x20);
      if ((((*(uint *)((int)param_1 + -0xc) & 0xffff) != 4) && (*(int *)((int)param_1 + -0xc) != 1))
         && (((*(uint *)((int)param_1 + -0xc) & 0xffff) != 2 &&
             ((*(int *)((int)param_1 + -0xc) != 3 &&
              (iVar2 = FUN_00573780(2,"dbgheap.c",0x41a,0,"_BLOCK_TYPE_IS_VALID(pHead->nBlockUse)"),
              iVar2 == 1)))))) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if ((DAT_007619c0 & 4) == 0) {
        iVar2 = FUN_0056fae0((int)param_1 + -4,DAT_007619cc,4);
        if ((iVar2 == 0) &&
           (iVar2 = FUN_00573780(1,0,0,0,"DAMAGE: before %hs block (#%d) at 0x%08X.\n",
                                 (&PTR_DAT_007619d0)[*(uint *)((int)param_1 + -0xc) & 0xffff],
                                 *(undefined4 *)((int)param_1 + -8),param_1), iVar2 == 1)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        iVar2 = FUN_0056fae0((int)param_1 + *(int *)((int)param_1 + -0x10),DAT_007619cc,4);
        if ((iVar2 == 0) &&
           (iVar2 = FUN_00573780(1,0,0,0,"DAMAGE: after %hs block (#%d) at 0x%08X.\n",
                                 (&PTR_DAT_007619d0)[*(uint *)((int)param_1 + -0xc) & 0xffff],
                                 *(undefined4 *)((int)param_1 + -8),param_1), iVar2 == 1)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      if (*(int *)((int)param_1 + -0xc) == 3) {
        if (((*(int *)((int)param_1 + -0x14) != -0x1234544) || (*(int *)((int)param_1 + -8) != 0))
           && (iVar2 = FUN_00573780(2,"dbgheap.c",0x42f,0,
                                    "pHead->nLine == IGNORE_LINE && pHead->lRequest == IGNORE_REQ"),
              iVar2 == 1)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        _memset(_Dst,(uint)DAT_007619cd,*(int *)((int)param_1 + -0x10) + 0x24);
        FUN_005787e0(_Dst);
      }
      else {
        if ((*(int *)((int)param_1 + -0xc) == 2) && (param_2 == 1)) {
          param_2 = 2;
        }
        if ((*(int *)((int)param_1 + -0xc) != param_2) &&
           (iVar2 = FUN_00573780(2,"dbgheap.c",0x43c,0,"pHead->nBlockUse == nBlockUse"), iVar2 == 1)
           ) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        DAT_0080a43c = DAT_0080a43c - *(int *)((int)param_1 + -0x10);
        if ((DAT_007619c0 & 2) == 0) {
          if (*_Dst == 0) {
            if ((DAT_0080a430 != _Dst) &&
               (iVar2 = FUN_00573780(2,"dbgheap.c",1099,0,"_pLastBlock == pHead"), iVar2 == 1)) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
            DAT_0080a430 = *(int **)((int)param_1 + -0x1c);
          }
          else {
            *(undefined4 *)(*_Dst + 4) = *(undefined4 *)((int)param_1 + -0x1c);
          }
          if (*(int *)((int)param_1 + -0x1c) == 0) {
            if ((DAT_0080a438 != _Dst) &&
               (iVar2 = FUN_00573780(2,"dbgheap.c",0x455,0,"_pFirstBlock == pHead"), iVar2 == 1)) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
            DAT_0080a438 = (int *)*_Dst;
          }
          else {
            **(int **)((int)param_1 + -0x1c) = *_Dst;
          }
          _memset(_Dst,(uint)DAT_007619cd,*(int *)((int)param_1 + -0x10) + 0x24);
          FUN_005787e0(_Dst);
        }
        else {
          *(undefined4 *)((int)param_1 + -0xc) = 0;
          _memset(param_1,(uint)DAT_007619cd,*(size_t *)((int)param_1 + -0x10));
        }
      }
    }
  }
  return;
}

