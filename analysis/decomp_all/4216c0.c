
void FUN__text__004216c0(int param_1,undefined4 param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00421e20(param_1);
  if (iVar2 == -1) {
    FUN__text__004225a0(0xffffffff);
    *(undefined4 *)(param_1 + 0x14) = 0;
    *(undefined4 *)(param_1 + 8) = local_8;
    *(undefined4 *)(param_1 + 0x18) = param_3;
    local_c = FUN__text__00421c70(param_1,param_2);
    if ((local_c == -1) &&
       (iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                    DAT_005ff5f4 + 0x12,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    FUN__text__0042b2d0("ERROR: already link task = %08x\n",param_1);
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff5f4 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4217b3;
  FUN__text__0056ce80();
  return;
}

