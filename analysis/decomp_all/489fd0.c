
void FUN__text__00489fd0(undefined4 param_1,undefined2 *param_2,undefined4 param_3)

{
  code *pcVar1;
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
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                              DAT_00618f68 + 1,0);
  if (iVar2 == 0) {
    local_c = FUN__text__004ddc60(param_3,*param_2);
    local_c = local_c & 0xff;
    local_8 = 0x48a047;
    FUN__text__0056ce80();
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

