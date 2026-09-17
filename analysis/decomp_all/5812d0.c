
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__005812d0(void)

{
  undefined2 uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  
  uVar1 = DAT_0080a65e;
  if (DAT_0080a634 == 0) {
    __free_dbg(DAT_0080a60c,2);
    __free_dbg(DAT_0080a610,2);
    __free_dbg(DAT_0080a614,2);
    DAT_0080a60c = 0;
    DAT_0080a610 = 0;
    DAT_0080a614 = 0;
    uVar5 = __malloc_dbg(2,2,"initnum.c",0x88);
    *(undefined4 *)PTR_PTR_00765250 = uVar5;
    if (*(int *)PTR_PTR_00765250 == 0) {
      uVar5 = 0xffffffff;
    }
    else {
      FUN__text__0056cd90(*(undefined4 *)PTR_PTR_00765250,&DAT_005c8218);
      uVar5 = __malloc_dbg(2,2,"initnum.c",0x8d);
      *(undefined4 *)(PTR_PTR_00765250 + 4) = uVar5;
      if (*(int *)(PTR_PTR_00765250 + 4) == 0) {
        uVar5 = 0xffffffff;
      }
      else {
        **(undefined1 **)(PTR_PTR_00765250 + 4) = 0;
        uVar5 = __malloc_dbg(2,2,"initnum.c",0x92);
        *(undefined4 *)(PTR_PTR_00765250 + 8) = uVar5;
        if (*(int *)(PTR_PTR_00765250 + 8) == 0) {
          uVar5 = 0xffffffff;
        }
        else {
          **(undefined1 **)(PTR_PTR_00765250 + 8) = 0;
          DAT_00764374 = **(undefined1 **)PTR_PTR_00765250;
          _DAT_00764378 = 1;
          uVar5 = 0;
        }
      }
    }
  }
  else {
    iVar2 = FUN__text__0058aa30(1,DAT_0080a65e,0xe,&DAT_0080a60c);
    iVar3 = FUN__text__0058aa30(1,uVar1,0xf,&DAT_0080a610);
    iVar4 = FUN__text__0058aa30(1,uVar1,0x10,&DAT_0080a614);
    fix_grouping(DAT_0080a614);
    if ((iVar2 == 0 && iVar3 == 0) && iVar4 == 0) {
      if (*(undefined **)PTR_PTR_00765250 != &DAT_00765218) {
        __free_dbg(*(undefined4 *)PTR_PTR_00765250,2);
        __free_dbg(*(undefined4 *)(PTR_PTR_00765250 + 4),2);
        __free_dbg(*(undefined4 *)(PTR_PTR_00765250 + 8),2);
      }
      *(undefined4 *)PTR_PTR_00765250 = DAT_0080a60c;
      *(undefined4 *)(PTR_PTR_00765250 + 4) = DAT_0080a610;
      *(undefined4 *)(PTR_PTR_00765250 + 8) = DAT_0080a614;
      DAT_00764374 = **(undefined1 **)PTR_PTR_00765250;
      _DAT_00764378 = 1;
      uVar5 = 0;
    }
    else {
      __free_dbg(DAT_0080a60c,2);
      __free_dbg(DAT_0080a610,2);
      __free_dbg(DAT_0080a614,2);
      DAT_0080a60c = 0;
      DAT_0080a610 = 0;
      DAT_0080a614 = 0;
      uVar5 = 0xffffffff;
    }
  }
  return uVar5;
}

