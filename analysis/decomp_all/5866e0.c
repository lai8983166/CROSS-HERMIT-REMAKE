
undefined4 __thiscall FUN__text__005866e0(undefined4 param_1,uint param_2)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  int iVar3;
  int *piVar4;
  
  if ((DAT_0080a900 <= param_2) ||
     ((*(byte *)((&DAT_0080a800)[(int)param_2 >> 5] + 4 + (param_2 & 0x1f) * 0x24) & 1) == 0)) {
    puVar1 = (undefined4 *)FUN__text__00576d20();
    *puVar1 = 9;
    return 0xffffffff;
  }
  FUN__text__00586620(param_2,param_1);
  if ((*(byte *)((&DAT_0080a800)[(int)param_2 >> 5] + 4 + (param_2 & 0x1f) * 0x24) & 1) != 0) {
    uVar2 = FUN__text__005864a0(param_2);
    iVar3 = (*API_KERNEL32_DLL_FlushFileBuffers)(uVar2);
    if (iVar3 == 0) {
      iVar3 = (*API_KERNEL32_DLL_GetLastError)();
    }
    else {
      iVar3 = 0;
    }
    if (iVar3 == 0) {
      uVar2 = 0;
      goto LAB__text__0058679f;
    }
    piVar4 = (int *)FUN__text__00576d30();
    *piVar4 = iVar3;
  }
  puVar1 = (undefined4 *)FUN__text__00576d20();
  *puVar1 = 9;
  uVar2 = 0xffffffff;
LAB__text__0058679f:
  FUN__text__005866b0(param_2);
  return uVar2;
}

