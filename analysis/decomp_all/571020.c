
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__00571020(undefined4 *param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 local_dc;
  undefined1 local_d4 [154];
  uint local_3a;
  int local_2c;
  undefined2 local_28;
  undefined2 uStack_26;
  undefined2 uStack_22;
  undefined2 local_20;
  undefined2 uStack_1e;
  undefined2 local_1c;
  short local_14;
  short sStack_12;
  undefined2 uStack_10;
  short sStack_e;
  short sStack_c;
  ushort local_a;
  undefined2 uStack_8;
  undefined2 uStack_6;
  
  (*API_KERNEL32_DLL_GetLocalTime)(&local_28);
  (*API_KERNEL32_DLL_GetSystemTime)(&local_14);
  if (((((uint)local_a == _DAT_0080a458 >> 0x10) && (sStack_c == DAT_0080a458)) &&
      (sStack_e == DAT_0080a456)) && ((sStack_12 == DAT_0080a452 && (local_14 == DAT_0080a450)))) {
    local_dc = DAT_0080a448;
  }
  else {
    iVar1 = (*API_KERNEL32_DLL_GetTimeZoneInformation)(local_d4);
    if (iVar1 == -1) {
      local_dc = 0xffffffff;
    }
    else if (((iVar1 == 2) && ((local_3a & 0xffff) != 0)) && (local_2c != 0)) {
      local_dc = 1;
    }
    else {
      local_dc = 0;
    }
    _DAT_0080a450 = CONCAT22(sStack_12,local_14);
    _DAT_0080a454 = CONCAT22(sStack_e,uStack_10);
    _DAT_0080a458 = CONCAT22(local_a,sStack_c);
    PTR_DAT_0080a45c = (undefined *)CONCAT22(uStack_6,uStack_8);
  }
  DAT_0080a448 = local_dc;
  uVar2 = FUN__text__0057c860(local_28,uStack_26,uStack_22,local_20,uStack_1e,local_1c,local_dc);
  if (param_1 != (undefined4 *)0x0) {
    *param_1 = uVar2;
  }
  return uVar2;
}

