
undefined4 * FUN_0056e920(uint param_1,uint param_2,int param_3,undefined4 param_4)

{
  code *pcVar1;
  bool bVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 *puVar5;
  int iVar6;
  
  bVar2 = false;
  if ((((DAT_007619c0 & 4) != 0) && (iVar4 = FUN_0056fb70(), iVar4 == 0)) &&
     (iVar4 = FUN_00573780(2,"dbgheap.c",0x14c,0,"_CrtCheckMemory()"), iVar4 == 1)) {
    pcVar1 = (code *)swi(3);
    puVar5 = (undefined4 *)(*pcVar1)();
    return puVar5;
  }
  iVar4 = DAT_007619c4;
  if (DAT_007619c4 == DAT_007619c8) {
    pcVar1 = (code *)swi(3);
    puVar5 = (undefined4 *)(*pcVar1)();
    return puVar5;
  }
  iVar6 = (*(code *)PTR_FUN_00762130)(1,0,param_1,param_2,DAT_007619c4,param_3,param_4);
  if (iVar6 == 0) {
    if (param_3 == 0) {
      iVar4 = FUN_00573780(0,0,0,0,&DAT_00592a18,"Client hook allocation failure.\n");
      if (iVar4 == 1) {
        pcVar1 = (code *)swi(3);
        puVar5 = (undefined4 *)(*pcVar1)();
        return puVar5;
      }
    }
    else {
      iVar4 = FUN_00573780(0,0,0,0,"Client hook allocation failure at file %hs line %d.\n",param_3,
                           param_4);
      if (iVar4 == 1) {
        pcVar1 = (code *)swi(3);
        puVar5 = (undefined4 *)(*pcVar1)();
        return puVar5;
      }
    }
    puVar5 = (undefined4 *)0x0;
  }
  else {
    if (((param_2 & 0xffff) != 2) && ((DAT_007619c0 & 1) == 0)) {
      bVar2 = true;
    }
    if ((param_1 < 0xffffffe1) && (param_1 + 0x24 < 0xffffffe1)) {
      if (((((param_2 & 0xffff) != 4) && (param_2 != 1)) && ((param_2 & 0xffff) != 2)) &&
         ((param_2 != 3 &&
          (iVar6 = FUN_00573780(1,0,0,0,&DAT_00592a18,
                                "Error: memory allocation: bad memory block type.\n"), iVar6 == 1)))
         ) {
        pcVar1 = (code *)swi(3);
        puVar5 = (undefined4 *)(*pcVar1)();
        return puVar5;
      }
      puVar5 = (undefined4 *)__heap_alloc_base(param_1 + 0x24);
      if (puVar5 == (undefined4 *)0x0) {
        puVar5 = (undefined4 *)0x0;
      }
      else {
        DAT_007619c4 = DAT_007619c4 + 1;
        if (bVar2) {
          *puVar5 = 0;
          puVar5[1] = 0;
          puVar5[2] = 0;
          puVar5[3] = 0xfedcbabc;
          puVar5[4] = param_1;
          puVar5[5] = 3;
          puVar5[6] = 0;
        }
        else {
          DAT_0080a434 = DAT_0080a434 + param_1;
          DAT_0080a43c = DAT_0080a43c + param_1;
          if (DAT_0080a440 < DAT_0080a43c) {
            DAT_0080a440 = DAT_0080a43c;
          }
          puVar3 = puVar5;
          if (DAT_0080a438 != (undefined4 *)0x0) {
            DAT_0080a438[1] = puVar5;
            puVar3 = DAT_0080a430;
          }
          DAT_0080a430 = puVar3;
          *puVar5 = DAT_0080a438;
          puVar5[1] = 0;
          puVar5[2] = param_3;
          puVar5[3] = param_4;
          puVar5[4] = param_1;
          puVar5[5] = param_2;
          puVar5[6] = iVar4;
          DAT_0080a438 = puVar5;
        }
        _memset(puVar5 + 7,(uint)DAT_007619cc,4);
        _memset((void *)((int)puVar5 + param_1 + 0x20),(uint)DAT_007619cc,4);
        _memset(puVar5 + 8,(uint)DAT_007619ce,param_1);
        puVar5 = puVar5 + 8;
      }
    }
    else {
      iVar4 = FUN_00573780(1,0,0,0,"Invalid allocation size: %u bytes.\n",param_1);
      if (iVar4 == 1) {
        pcVar1 = (code *)swi(3);
        puVar5 = (undefined4 *)(*pcVar1)();
        return puVar5;
      }
      puVar5 = (undefined4 *)0x0;
    }
  }
  return puVar5;
}

