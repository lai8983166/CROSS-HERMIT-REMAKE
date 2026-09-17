
undefined4 __thiscall
FUN__text__0052d4bb(undefined4 *param_1,undefined4 param_2,int param_3,undefined4 *param_4,
                   undefined4 param_5)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  int local_24 [8];
  
  local_24[0] = 0;
  local_24[1] = 5;
  local_24[2] = 4;
  local_24[3] = 1;
  local_24[4] = 3;
  local_24[5] = 2;
  local_24[6] = 6;
  local_24[7] = 0;
  iVar2 = param_3;
  do {
    param_1[0x10] = param_5;
    iVar1 = local_24[local_24[7]];
    param_1[0x12] = iVar1;
    param_1[0x11] = 3;
    if (iVar1 == 0) {
      iVar2 = FUN__text__0052d48b(param_2,param_3);
    }
    else if (iVar1 == 1) {
      iVar2 = FUN__text__0052bc56(param_2,param_3);
    }
    else if (iVar1 == 2) {
      iVar2 = FUN__text__0052bec6(param_2,param_3);
    }
    else if (iVar1 == 3) {
      iVar2 = FUN__text__0052c643(param_2,param_3);
    }
    else if (iVar1 == 4) {
      iVar2 = FUN__text__0052cbd9(param_2,param_3);
    }
    else if (iVar1 == 5) {
      iVar2 = FUN__text__0052c36d(param_2,param_3);
    }
    else if (iVar1 == 6) {
      iVar2 = FUN__text__0052b1fa(param_2,param_3);
    }
    if (-1 < iVar2) break;
    if ((param_1[1] != 0) && (param_1[0xe] != 0)) {
      FUN__text__00428ad0(param_1[1]);
    }
    if ((param_1[2] != 0) && (param_1[0xf] != 0)) {
      FUN__text__00428ad0(param_1[2]);
    }
    if (param_1[0x13] != 0) {
      FUN__text__0052b11b(1);
    }
    if (param_1[0x14] != 0) {
      FUN__text__0052b11b(1);
    }
    local_24[7] = local_24[7] + 1;
    param_1[1] = 0;
    param_1[2] = 0;
    param_1[0xe] = 0;
    param_1[0xf] = 0;
    param_1[0x13] = 0;
    param_1[0x14] = 0;
  } while ((uint)local_24[7] < 7);
  iVar2 = 7;
  if (local_24[7] == 7) {
    uVar3 = 0x88760b59;
  }
  else {
    puVar5 = param_4;
    puVar4 = param_1;
    if (param_4 != (undefined4 *)0x0) {
      for (; iVar2 != 0; iVar2 = iVar2 + -1) {
        *puVar5 = 0;
        puVar5 = puVar5 + 1;
      }
      *param_4 = param_1[3];
      param_4[1] = param_1[4];
      param_4[2] = param_1[5];
      param_4[3] = 1;
      uVar3 = FUN__text__00526e2f(*param_1);
      param_4[4] = uVar3;
      param_4[5] = param_1[0x11];
      param_4[6] = param_1[0x12];
      for (puVar5 = param_1; puVar5[0x13] != 0; puVar5 = (undefined4 *)puVar5[0x13]) {
        param_4[3] = param_4[3] + 1;
      }
    }
    do {
      for (; param_1 != (undefined4 *)0x0; param_1 = (undefined4 *)param_1[0x13]) {
        param_1[8] = param_1[3];
        param_1[9] = param_1[4];
        param_1[6] = 0;
        param_1[7] = 0;
        param_1[10] = 0;
        param_1[0xb] = param_1[5];
      }
      param_1 = (undefined4 *)puVar4[0x14];
      puVar4 = param_1;
    } while (param_1 != (undefined4 *)0x0);
    uVar3 = 0;
  }
  return uVar3;
}

