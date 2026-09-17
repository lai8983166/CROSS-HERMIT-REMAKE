
undefined4 __fastcall FUN__text__00581600(undefined4 param_1)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  int iVar3;
  
  if (DAT_0080a630 == 0) {
    PTR_DAT_00765220 = *(undefined **)PTR_PTR_00765250;
    PTR_DAT_00765224 = *(undefined **)(PTR_PTR_00765250 + 4);
    PTR_DAT_00765228 = *(undefined **)(PTR_PTR_00765250 + 8);
    PTR_PTR_00765250 = (undefined *)&PTR_DAT_00765220;
    FUN__text__005819c0(DAT_0080a618,param_1);
    __free_dbg(DAT_0080a618,2);
    DAT_0080a618 = (undefined4 *)0x0;
    uVar2 = 0;
  }
  else {
    puVar1 = (undefined4 *)__calloc_dbg(1,0x30,2,"initmon.c",0x4a);
    if (puVar1 == (undefined4 *)0x0) {
      uVar2 = 1;
    }
    else {
      iVar3 = FUN__text__00581730(puVar1);
      if (iVar3 == 0) {
        *puVar1 = *(undefined4 *)PTR_PTR_00765250;
        puVar1[1] = *(undefined4 *)(PTR_PTR_00765250 + 4);
        puVar1[2] = *(undefined4 *)(PTR_PTR_00765250 + 8);
        PTR_PTR_00765250 = (undefined *)puVar1;
        FUN__text__005819c0(DAT_0080a618);
        __free_dbg(DAT_0080a618,2);
        DAT_0080a618 = puVar1;
        uVar2 = 0;
      }
      else {
        FUN__text__005819c0(puVar1);
        __free_dbg(puVar1,2);
        uVar2 = 1;
      }
    }
  }
  return uVar2;
}

