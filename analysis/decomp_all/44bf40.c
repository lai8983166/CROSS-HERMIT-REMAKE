
void FUN__text__0044bf40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 0) || (1 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=type) && (type<=1)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606774 + 4,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_18 = FUN__text__0044bed0(param_1);
  local_14 = 0x40;
  local_10 = 0;
  for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
    if (*(short *)(local_18 + local_c * 2) != 0) {
      local_10 = local_10 + 1;
    }
  }
  local_8 = 0x44bfed;
  FUN__text__0056ce80();
  return;
}

