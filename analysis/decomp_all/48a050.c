
void FUN__text__0048a050(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                              DAT_00618f6c + 1,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = (uint)*(byte *)(param_1 + 2);
  switch(local_10) {
  case 0:
    local_c = (uint)*(byte *)(*(int *)(param_3 + 600) + 0x44);
    break;
  case 1:
    local_c = (uint)*(byte *)(*(int *)(param_3 + 600) + 0x44);
    break;
  case 2:
    local_c = (uint)*(byte *)(*(int *)(param_3 + 600) + 0x44) + (uint)*(byte *)(param_2 + 0x16) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (uint)*(byte *)(param_2 + 0x17)) / 100
    ;
    break;
  case 3:
    local_c = (uint)*(byte *)(param_2 + 0x16) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (uint)*(byte *)(param_2 + 0x17)) / 100
    ;
    break;
  case 4:
    local_c = (uint)*(byte *)(*(int *)(param_3 + 600) + 0x44) + (uint)*(byte *)(param_2 + 0x16) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (uint)*(byte *)(param_2 + 0x17)) / 100
    ;
    break;
  case 5:
    local_c = (uint)*(byte *)(param_2 + 0x16) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (uint)*(byte *)(param_2 + 0x17)) / 100
    ;
    break;
  case 6:
    local_c = (uint)*(byte *)(param_2 + 0x16) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 10) * (uint)*(byte *)(param_2 + 0x17)) /
              100;
  }
  if ((int)local_c < 0x21) {
    if ((int)local_c < 0) {
      local_c = 0;
    }
  }
  else {
    local_c = 0x20;
  }
  local_8 = 0x48a231;
  FUN__text__0056ce80();
  return;
}

