
undefined4 __thiscall FUN__text__005863c0(undefined4 param_1,uint param_2)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  
  if (((param_2 < DAT_0080a900) &&
      (iVar3 = (int)param_2 >> 5,
      (*(byte *)((&DAT_0080a800)[iVar3] + 4 + (param_2 & 0x1f) * 0x24) & 1) != 0)) &&
     (*(int *)((&DAT_0080a800)[iVar3] + (param_2 & 0x1f) * 0x24) != -1)) {
    if (DAT_007619fc == 1) {
      if (param_2 == 0) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff6,0);
      }
      else if (param_2 == 1) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff5,0);
      }
      else if (param_2 == 2) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff4,0);
      }
    }
    *(undefined4 *)((&DAT_0080a800)[iVar3] + (param_2 & 0x1f) * 0x24) = 0xffffffff;
    uVar1 = 0;
  }
  else {
    puVar2 = (undefined4 *)FUN__text__00576d20(param_1);
    *puVar2 = 9;
    puVar2 = (undefined4 *)FUN__text__00576d30();
    *puVar2 = 0;
    uVar1 = 0xffffffff;
  }
  return uVar1;
}

