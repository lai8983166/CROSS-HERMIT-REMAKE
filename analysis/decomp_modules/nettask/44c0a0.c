
void FUN__text__0044c0a0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
    if (*(short *)(param_1 + local_c * 2) != 0) {
      if (local_10 == param_2) goto LAB__text__0044c131;
      local_10 = local_10 + 1;
    }
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                              DAT_0060677c + 0x14,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__0044c131:
  local_8 = 0x44c13e;
  FUN__text__0056ce80();
  return;
}

