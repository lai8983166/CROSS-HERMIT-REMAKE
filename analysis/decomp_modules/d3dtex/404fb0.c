
void FUN__text__00404fb0(undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,
                        undefined4 param_5,undefined4 param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_3;
  iVar2 = FUN__text__00420b50(param_3);
  if (iVar2 == 0) {
    local_10 = *(ushort *)(local_c + 2) & 7;
    if (local_10 == 1) {
      *(undefined4 *)(local_8 + 0x34) = 0x29;
      *(undefined2 *)(local_8 + 0x38) = *(undefined2 *)(local_c + 4);
      *(undefined2 *)(local_8 + 0x3a) = *(undefined2 *)(local_c + 6);
      iVar2 = FUN__text__00403bd0(param_1,0);
      if (iVar2 == 0) {
        FUN__text__00404690(param_3,param_4,param_6);
      }
    }
    else if (local_10 == 2) {
      *(undefined4 *)(local_8 + 0x34) = 0x19;
      *(undefined2 *)(local_8 + 0x38) = *(undefined2 *)(local_c + 4);
      *(undefined2 *)(local_8 + 0x3a) = *(undefined2 *)(local_c + 6);
      iVar2 = FUN__text__00403bd0(param_1,0);
      if (iVar2 == 0) {
        FUN__text__004046f0(param_3,param_4,param_6);
      }
    }
    else if ((local_10 == 4) &&
            (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                         "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                         DAT_005ff0a4 + 0x2c,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x405123;
  FUN__text__0056ce80();
  return;
}

