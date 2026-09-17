
void FUN__text__00472550(int param_1,int param_2,int param_3)

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
  local_10 = param_2;
  if (param_2 == 0) {
    local_c = *(short *)(*(int *)(param_1 + 600) + 0x16) + param_3;
    if (0x7fff < local_c) {
      local_c = 0x7fff;
    }
    if ((((*(short *)(*(int *)(param_1 + 600) + 0x54) != 0) && (local_c < 1)) && (param_3 < 0)) &&
       (((int)(uint)*(ushort *)(*(int *)(param_1 + 600) + 0x54) <=
         (int)*(short *)(*(int *)(param_1 + 600) + 0x16) &&
        ((int)(uint)*(ushort *)(*(int *)(param_1 + 600) + 0x54) <= -param_3)))) {
      local_c = 1;
    }
    if (local_c < 0) {
      local_c = 0;
    }
    else if (*(short *)(*(int *)(param_1 + 600) + 0x14) < local_c) {
      local_c = (int)*(short *)(*(int *)(param_1 + 600) + 0x14);
    }
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x16) = (undefined2)local_c;
  }
  else if (param_2 == 1) {
    local_c = *(short *)(*(int *)(param_1 + 600) + 0x1c) + param_3;
    if (0x7fff < local_c) {
      local_c = 0x7fff;
    }
    if (local_c < 0) {
      local_c = 0;
    }
    else if (*(short *)(*(int *)(param_1 + 600) + 0x1a) < local_c) {
      local_c = (int)*(short *)(*(int *)(param_1 + 600) + 0x1a);
    }
    *(undefined2 *)(*(int *)(param_1 + 600) + 0x1c) = (undefined2)local_c;
  }
  else if (param_2 == 2) {
    local_c = *(int *)(*(int *)(param_1 + 600) + 0x24) + param_3;
    if (local_c < 0) {
      local_c = 0;
    }
    else if (*(int *)(*(int *)(param_1 + 600) + 0x20) < local_c) {
      local_c = *(int *)(*(int *)(param_1 + 600) + 0x20);
    }
    *(int *)(*(int *)(param_1 + 600) + 0x24) = local_c;
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618c34 + 0x2f,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x472763;
  FUN__text__0056ce80();
  return;
}

