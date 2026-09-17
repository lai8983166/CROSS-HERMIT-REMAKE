
void FUN__text1__0084234e(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  char local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_8;
  
  iVar1 = *param_2;
  iVar2 = *(int *)param_2[2];
  local_8 = *(int *)(param_2[2] + 0xc);
  local_1c = -1;
  *(undefined4 *)(param_1 + 0x1448) = 0;
  *(undefined4 *)(param_1 + 0x144c) = 0x23d;
  for (local_20 = 0; local_20 < local_8; local_20 = local_20 + 1) {
    if (*(short *)(iVar1 + local_20 * 4) == 0) {
      *(undefined2 *)(iVar1 + 2 + local_20 * 4) = 0;
    }
    else {
      local_1c = local_20;
      *(int *)(param_1 + 0x1448) = *(int *)(param_1 + 0x1448) + 1;
      *(int *)(param_1 + 0xb54 + *(int *)(param_1 + 0x1448) * 4) = local_20;
      *(undefined1 *)(param_1 + local_20 + 0x1450) = 0;
    }
  }
  while (*(int *)(param_1 + 0x1448) < 2) {
    if (local_1c < 2) {
      local_24 = local_1c + 1;
      local_1c = local_24;
    }
    else {
      local_24 = 0;
    }
    *(int *)(param_1 + 0x1448) = *(int *)(param_1 + 0x1448) + 1;
    *(int *)(param_1 + 0xb54 + *(int *)(param_1 + 0x1448) * 4) = local_24;
    *(undefined2 *)(iVar1 + local_24 * 4) = 1;
    *(undefined1 *)(param_1 + local_24 + 0x1450) = 0;
    *(int *)(param_1 + 0x16a0) = *(int *)(param_1 + 0x16a0) + -1;
    if (iVar2 != 0) {
      *(uint *)(param_1 + 0x16a4) =
           *(int *)(param_1 + 0x16a4) - (uint)*(ushort *)(iVar2 + 2 + local_24 * 4);
    }
  }
  param_2[1] = local_1c;
  for (local_20 = *(int *)(param_1 + 0x1448) / 2; 0 < local_20; local_20 = local_20 + -1) {
    FUN__text1__008426ee(param_1,iVar1,local_20);
  }
  do {
    iVar2 = *(int *)(param_1 + 0xb58);
    *(undefined4 *)(param_1 + 0xb58) =
         *(undefined4 *)(param_1 + 0xb54 + *(int *)(param_1 + 0x1448) * 4);
    *(int *)(param_1 + 0x1448) = *(int *)(param_1 + 0x1448) + -1;
    FUN__text1__008426ee(param_1,iVar1,1);
    iVar3 = *(int *)(param_1 + 0xb58);
    *(int *)(param_1 + 0x144c) = *(int *)(param_1 + 0x144c) + -1;
    *(int *)(param_1 + 0xb54 + *(int *)(param_1 + 0x144c) * 4) = iVar2;
    *(int *)(param_1 + 0x144c) = *(int *)(param_1 + 0x144c) + -1;
    *(int *)(param_1 + 0xb54 + *(int *)(param_1 + 0x144c) * 4) = iVar3;
    *(short *)(iVar1 + local_8 * 4) = *(short *)(iVar1 + iVar2 * 4) + *(short *)(iVar1 + iVar3 * 4);
    if (*(byte *)(param_1 + iVar2 + 0x1450) < *(byte *)(param_1 + iVar3 + 0x1450)) {
      local_28 = *(char *)(param_1 + iVar3 + 0x1450);
    }
    else {
      local_28 = *(char *)(param_1 + iVar2 + 0x1450);
    }
    *(char *)(param_1 + local_8 + 0x1450) = local_28 + '\x01';
    *(undefined2 *)(iVar1 + 2 + iVar3 * 4) = (undefined2)local_8;
    *(undefined2 *)(iVar1 + 2 + iVar2 * 4) = (undefined2)local_8;
    *(int *)(param_1 + 0xb58) = local_8;
    local_8 = local_8 + 1;
    FUN__text1__008426ee(param_1,iVar1,1);
  } while (1 < *(int *)(param_1 + 0x1448));
  *(int *)(param_1 + 0x144c) = *(int *)(param_1 + 0x144c) + -1;
  *(undefined4 *)(param_1 + 0xb54 + *(int *)(param_1 + 0x144c) * 4) =
       *(undefined4 *)(param_1 + 0xb58);
  FUN__text1__0084288d(param_1,param_2);
  FUN__text1__00842bc0(iVar1,local_1c,param_1 + 0xb34);
  return;
}

