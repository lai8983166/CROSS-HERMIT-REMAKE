
void FUN__text__00420ca0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  local_10 = *(ushort *)(param_1 + 2) & 7;
  if (local_10 != 1) {
    if (local_10 == 2) {
      local_c = (uint)*(ushort *)(param_1 + 8) * 2 * (uint)*(ushort *)(param_1 + 10) + 0xc;
      goto LAB__text__00420d64;
    }
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\Format.cpp",
                                DAT_005ff5e4 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  iVar2 = (uint)*(ushort *)(param_1 + 8) * (uint)*(ushort *)(param_1 + 10);
  local_c = iVar2 + 0xc;
  if ((*(ushort *)(param_1 + 2) & 0x8000) != 0) {
    local_c = iVar2 + 0x40c;
  }
LAB__text__00420d64:
  local_8 = 0x420d74;
  FUN__text__0056ce80();
  return;
}

