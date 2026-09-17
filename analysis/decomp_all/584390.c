
undefined4 FUN_00584390(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 uVar2;
  int local_8;
  
  local_8 = 0;
  if (DAT_0080a6a0 == (code *)0x0) {
    iVar1 = (*DAT_00592184)("user32.dll");
    if (iVar1 != 0) {
      DAT_0080a6a0 = (code *)(*DAT_005922cc)(iVar1,"MessageBoxA");
      if (DAT_0080a6a0 != (code *)0x0) {
        DAT_0080a6a4 = (code *)(*DAT_005922cc)(iVar1,"GetActiveWindow");
        DAT_0080a6a8 = (code *)(*DAT_005922cc)(iVar1,"GetLastActivePopup");
        goto LAB_00584403;
      }
    }
    uVar2 = 0;
  }
  else {
LAB_00584403:
    if (DAT_0080a6a4 != (code *)0x0) {
      local_8 = (*DAT_0080a6a4)();
    }
    if ((local_8 != 0) && (DAT_0080a6a8 != (code *)0x0)) {
      local_8 = (*DAT_0080a6a8)(local_8);
    }
    uVar2 = (*DAT_0080a6a0)(local_8,param_1,param_2,param_3);
  }
  return uVar2;
}

