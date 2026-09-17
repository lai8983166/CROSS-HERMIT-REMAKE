
void FUN__text__00482810(ushort *param_1)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1[1] == 0) {
    local_c = (uint)*param_1;
  }
  else {
    uVar1 = *param_1;
    iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618efc + 5);
    local_c = (uint)uVar1 + iVar2 % (int)(uint)param_1[1];
  }
  *(uint *)(param_1 + 0x14) = local_c;
  local_8 = 0x482897;
  FUN__text__0056ce80();
  return;
}

