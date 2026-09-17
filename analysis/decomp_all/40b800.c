
void FUN__text__0040b800(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (DAT_00791730 < 0x800) {
    *(undefined4 *)(&DAT_00791734 + DAT_00791730 * 4) = param_1;
    DAT_00791730 = DAT_00791730 + 1;
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                DAT_005ff108 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x40b884;
  FUN__text__0056ce80();
  return;
}

