
uint FUN__text__005890a0(ushort *param_1,byte *param_2,uint param_3)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  
  if (((DAT_00764370 != 1) && (DAT_00764370 != 2)) &&
     (iVar2 = FUN__text__00573780(2,"mbtowc.c",0x4f,0,"MB_CUR_MAX == 1 || MB_CUR_MAX == 2"),
     iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_2 == (byte *)0x0) || (param_3 == 0)) {
    uVar3 = 0;
  }
  else if (*param_2 == 0) {
    if (param_1 != (ushort *)0x0) {
      *param_1 = 0;
    }
    uVar3 = 0;
  }
  else if (DAT_0080a62c == 0) {
    if (param_1 != (ushort *)0x0) {
      *param_1 = (ushort)*param_2;
    }
    uVar3 = 1;
  }
  else if ((*(ushort *)(PTR_DAT_00764164 + (uint)*param_2 * 2) & 0x8000) == 0) {
    iVar2 = (*API_KERNEL32_DLL_MultiByteToWideChar)
                      (DAT_0080a63c,9,param_2,1,param_1,param_1 != (ushort *)0x0);
    if (iVar2 == 0) {
      puVar4 = (undefined4 *)FUN__text__00576d20();
      *puVar4 = 0x2a;
      uVar3 = 0xffffffff;
    }
    else {
      uVar3 = 1;
    }
  }
  else if (((((int)DAT_00764370 < 2) || ((int)param_3 < (int)DAT_00764370)) ||
           (iVar2 = (*API_KERNEL32_DLL_MultiByteToWideChar)
                              (DAT_0080a63c,9,param_2,DAT_00764370,param_1,param_1 != (ushort *)0x0)
           , uVar3 = DAT_00764370, iVar2 == 0)) &&
          ((param_3 < DAT_00764370 || (uVar3 = DAT_00764370, param_2[1] == 0)))) {
    puVar4 = (undefined4 *)FUN__text__00576d20();
    *puVar4 = 0x2a;
    uVar3 = 0xffffffff;
  }
  return uVar3;
}

