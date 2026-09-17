
void FUN__text__00421c70(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int *local_14;
  int *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00421e20(param_1);
  if (iVar2 == -1) {
    local_10 = (int *)(local_8 + param_2 * 8);
    local_c = *local_10;
    while (*local_10 != 0) {
      local_c = *local_10;
      local_10 = (int *)(local_c + 0xc);
    }
    local_14 = (int *)(param_1 + 0xc);
    *local_14 = *local_10;
    *local_10 = param_1;
  }
  else {
    FUN__text__0042b2d0("ERROR: already link task = %08x\n",param_1);
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff5fc + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x421d3b;
  FUN__text__0056ce80();
  return;
}

