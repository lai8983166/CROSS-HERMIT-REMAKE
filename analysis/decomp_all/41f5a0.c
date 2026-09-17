
void __thiscall FUN__text__0041f5a0(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_2 < 0x100) && (param_3 < *(int *)(param_1 + 4 + param_2 * 8))) {
    local_c = *(int *)(param_1 + param_2 * 8);
    local_10 = local_c + param_3 * 0x54;
    local_8 = param_1;
    if ((local_10 == 0) &&
       (iVar2 = FUN__text__00424f80("tex!=0",
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                                    DAT_005ff5d8 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(int *)(local_10 + 0x2c) == -0x32323233) &&
       (iVar2 = FUN__text__00424f80("(uint32)tex->pTex!=0xcdcdcdcd",
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                                    DAT_005ff5d8 + 9,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x41f664;
  FUN__text__0056ce80();
  return;
}

