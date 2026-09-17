
void FUN__text__00492680(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  char *local_14;
  int local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),1);
  if (*(char *)(param_2 + 0x14) != '\0') {
    if (*(byte *)(*(int *)(param_1 + 600) + 7) < 0x1f) {
      local_14 = "dddK#\x0fddddK#dddddKdddddddddddd";
    }
    else if (*(byte *)(*(int *)(param_1 + 600) + 7) < 0x33) {
      local_14 = "ddddK#dddddKdddddddddddd";
    }
    else if (*(byte *)(*(int *)(param_1 + 600) + 7) < 0x4c) {
      local_14 = "dddddKdddddddddddd";
    }
    else if (*(byte *)(*(int *)(param_1 + 600) + 7) < 0x5b) {
      local_14 = "dddddddddddd";
    }
    else {
      local_14 = "dddddd";
    }
    local_c = &DAT_006f4088 + (uint)*(byte *)(param_2 + 0x14) * 0x10;
    local_10 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                   DAT_00619254 + 0x1c);
    local_10 = local_10 % 100;
    if (local_10 < local_14[(byte)local_c[3]]) {
      FUN__text__004902e0(param_2,param_2 + 0x14,0);
      FUN__text__00495130(param_2,1);
    }
  }
  local_8 = 0x4927b5;
  FUN__text__0056ce80();
  return;
}

