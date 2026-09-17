
void __thiscall FUN__text__004046f0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_14 = param_2;
    local_8 = param_1;
    if (((*(ushort *)(param_2 + 2) & 7) != 2) &&
       (iVar2 = FUN__text__00424f80("(dxp_head->mode&(0x0001|0x0002|0x0004)) == 0x0002",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff09c + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(short *)(local_8 + 0x3c) != *(short *)(local_14 + 8)) &&
       (iVar2 = FUN__text__00424f80("imgtw == (sint16)dxp_head->tw",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff09c + 0xb,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(short *)(local_8 + 0x3e) != *(short *)(local_14 + 10)) &&
       (iVar2 = FUN__text__00424f80("imgth == (sint16)dxp_head->th",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff09c + 0xc,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    iVar2 = FUN__text__00403910(&local_10);
    if (iVar2 == 0) {
      for (local_18 = 0; local_18 != *(ushort *)(local_14 + 10); local_18 = local_18 + 1) {
        local_1c = local_14 + 0xc + (uint)*(ushort *)(local_14 + 8) * 2 * local_18;
        local_20 = local_c + local_10 * local_18;
        FUN__text__0056d4d0(local_20,local_1c,(uint)*(ushort *)(local_14 + 8) << 1);
      }
      FUN__text__00403990();
    }
  }
  local_8 = 0x404866;
  FUN__text__0056ce80();
  return;
}

