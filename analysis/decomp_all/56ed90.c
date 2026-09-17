
int * FUN__text__0056ed90(int param_1,uint param_2,uint param_3,int param_4,int param_5,int param_6)

{
  code *pcVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  bool bVar6;
  int *local_10;
  
  if (param_1 == 0) {
    piVar2 = (int *)__malloc_dbg(param_2,param_3,param_4,param_5);
  }
  else if ((param_6 == 0) || (param_2 != 0)) {
    if (((DAT_007619c0 & 4) != 0) &&
       ((iVar3 = FUN__text__0056fb70(), iVar3 == 0 &&
        (iVar3 = FUN__text__00573780(2,"dbgheap.c",0x246,0,"_CrtCheckMemory()"), iVar3 == 1)))) {
      pcVar1 = (code *)swi(3);
      piVar4 = (int *)(*pcVar1)();
      return piVar4;
    }
    iVar3 = DAT_007619c4;
    if (DAT_007619c4 == DAT_007619c8) {
      pcVar1 = (code *)swi(3);
      piVar4 = (int *)(*pcVar1)();
      return piVar4;
    }
    iVar5 = (*(code *)PTR_FUN_00762130)(2,param_1,param_2,param_3,DAT_007619c4,param_4,param_5);
    if (iVar5 == 0) {
      if (param_4 == 0) {
        iVar3 = FUN__text__00573780(0,0,0,0,&DAT_00592a18,"Client hook re-allocation failure.\n");
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          piVar4 = (int *)(*pcVar1)();
          return piVar4;
        }
      }
      else {
        iVar3 = FUN__text__00573780(0,0,0,0,
                                    "Client hook re-allocation failure at file %hs line %d.\n",
                                    param_4,param_5);
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          piVar4 = (int *)(*pcVar1)();
          return piVar4;
        }
      }
      piVar2 = (int *)0x0;
    }
    else if (param_2 < 0xffffffdc) {
      if ((((param_3 != 1) && ((param_3 & 0xffff) != 4)) && ((param_3 & 0xffff) != 2)) &&
         (iVar5 = FUN__text__00573780(1,0,0,0,&DAT_00592a18,
                                      "Error: memory allocation: bad memory block type.\n"),
         iVar5 == 1)) {
        pcVar1 = (code *)swi(3);
        piVar4 = (int *)(*pcVar1)();
        return piVar4;
      }
      iVar5 = FUN__text__00570050(param_1);
      if ((iVar5 == 0) &&
         (iVar5 = FUN__text__00573780(2,"dbgheap.c",0x26e,0,"_CrtIsValidHeapPointer(pUserData)"),
         iVar5 == 1)) {
        pcVar1 = (code *)swi(3);
        piVar4 = (int *)(*pcVar1)();
        return piVar4;
      }
      piVar4 = (int *)(param_1 + -0x20);
      bVar6 = *(int *)(param_1 + -0xc) == 3;
      if (bVar6) {
        if (((*(int *)(param_1 + -0x14) != -0x1234544) || (*(int *)(param_1 + -8) != 0)) &&
           (iVar5 = FUN__text__00573780(2,"dbgheap.c",0x278,0,
                                        "pOldBlock->nLine == IGNORE_LINE && pOldBlock->lRequest == IGNORE_REQ"
                                       ), iVar5 == 1)) {
          pcVar1 = (code *)swi(3);
          piVar4 = (int *)(*pcVar1)();
          return piVar4;
        }
      }
      else {
        if (((*(uint *)(param_1 + -0xc) & 0xffff) == 2) && ((param_3 & 0xffff) == 1)) {
          param_3 = 2;
        }
        if (((*(uint *)(param_1 + -0xc) & 0xffff) != (param_3 & 0xffff)) &&
           (iVar5 = FUN__text__00573780(2,"dbgheap.c",0x27f,0,
                                        "_BLOCK_TYPE(pOldBlock->nBlockUse)==_BLOCK_TYPE(nBlockUse)")
           , iVar5 == 1)) {
          pcVar1 = (code *)swi(3);
          piVar4 = (int *)(*pcVar1)();
          return piVar4;
        }
      }
      if (param_6 == 0) {
        local_10 = (int *)FUN__text__00578130(piVar4,param_2 + 0x24);
        if (local_10 == (int *)0x0) {
          return (int *)0x0;
        }
      }
      else {
        local_10 = (int *)FUN__text__00578340(piVar4,param_2 + 0x24);
        if (local_10 == (int *)0x0) {
          return (int *)0x0;
        }
      }
      DAT_007619c4 = DAT_007619c4 + 1;
      if (!bVar6) {
        DAT_0080a434 = (DAT_0080a434 - local_10[4]) + param_2;
        DAT_0080a43c = (DAT_0080a43c - local_10[4]) + param_2;
        if (DAT_0080a440 < DAT_0080a43c) {
          DAT_0080a440 = DAT_0080a43c;
        }
      }
      piVar2 = local_10 + 8;
      if ((uint)local_10[4] < param_2) {
        _memset((void *)((int)piVar2 + local_10[4]),(uint)DAT_007619ce,param_2 - local_10[4]);
      }
      _memset((void *)((int)piVar2 + param_2),(uint)DAT_007619cc,4);
      if (!bVar6) {
        local_10[2] = param_4;
        local_10[3] = param_5;
        local_10[6] = iVar3;
      }
      local_10[4] = param_2;
      if (((param_6 == 0) && (local_10 != piVar4)) &&
         (iVar3 = FUN__text__00573780(2,"dbgheap.c",0x2b5,0,
                                      "fRealloc || (!fRealloc && pNewBlock == pOldBlock)"),
         iVar3 == 1)) {
        pcVar1 = (code *)swi(3);
        piVar4 = (int *)(*pcVar1)();
        return piVar4;
      }
      if ((local_10 != piVar4) && (!bVar6)) {
        if (*local_10 == 0) {
          if ((DAT_0080a430 != piVar4) &&
             (iVar3 = FUN__text__00573780(2,"dbgheap.c",0x2c4,0,"_pLastBlock == pOldBlock"),
             iVar3 == 1)) {
            pcVar1 = (code *)swi(3);
            piVar4 = (int *)(*pcVar1)();
            return piVar4;
          }
          DAT_0080a430 = (int *)local_10[1];
        }
        else {
          *(int *)(*local_10 + 4) = local_10[1];
        }
        if (local_10[1] == 0) {
          if ((DAT_0080a438 != piVar4) &&
             (iVar3 = FUN__text__00573780(2,"dbgheap.c",0x2cf,0,"_pFirstBlock == pOldBlock"),
             iVar3 == 1)) {
            pcVar1 = (code *)swi(3);
            piVar4 = (int *)(*pcVar1)();
            return piVar4;
          }
          DAT_0080a438 = (int *)*local_10;
        }
        else {
          *(int *)local_10[1] = *local_10;
        }
        if (DAT_0080a438 == (int *)0x0) {
          DAT_0080a430 = local_10;
        }
        else {
          DAT_0080a438[1] = (int)local_10;
        }
        *local_10 = (int)DAT_0080a438;
        local_10[1] = 0;
        DAT_0080a438 = local_10;
      }
    }
    else {
      iVar3 = FUN__text__00573780(1,0,0,0,"Allocation too large or negative: %u bytes.\n",param_2);
      if (iVar3 == 1) {
        pcVar1 = (code *)swi(3);
        piVar4 = (int *)(*pcVar1)();
        return piVar4;
      }
      piVar2 = (int *)0x0;
    }
  }
  else {
    __free_dbg(param_1,param_3);
    piVar2 = (int *)0x0;
  }
  return piVar2;
}

