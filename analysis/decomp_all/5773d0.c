
/* Library Function - Single Match
    __close_lk
   
   Library: Visual Studio 2003 Debug */

undefined4 __close_lk(uint param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  ulong local_8;
  
  iVar1 = FUN__text__005864a0(param_1);
  if (iVar1 != -1) {
    if ((param_1 == 1) || (param_1 == 2)) {
      iVar1 = FUN__text__005864a0(1);
      iVar2 = FUN__text__005864a0(2);
      if (iVar1 == iVar2) goto LAB__text__00577423;
    }
    uVar3 = FUN__text__005864a0(param_1);
    iVar1 = (*DAT_00592270)(uVar3);
    if (iVar1 == 0) {
      local_8 = (*API_KERNEL32_DLL_GetLastError)();
      goto LAB__text__00577435;
    }
  }
LAB__text__00577423:
  local_8 = 0;
LAB__text__00577435:
  FUN__text__005863c0(param_1);
  *(undefined1 *)((&DAT_0080a800)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) = 0;
  if (local_8 == 0) {
    uVar3 = 0;
  }
  else {
    __dosmaperr(local_8);
    uVar3 = 0xffffffff;
  }
  return uVar3;
}

