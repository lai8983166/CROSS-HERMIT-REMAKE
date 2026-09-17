
void FUN__text1__00810105(int param_1,int param_2,int param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  
  if (*(int *)(param_1 + 0x414 + param_2 * 0x10) == 0) {
    *(int *)(param_1 + 0x410 + *(int *)(param_1 + 0x418 + param_2 * 0x10) * 0x10) = param_3;
    *(int *)(param_1 + 0x410 + (*(int *)(param_1 + 0x418 + param_2 * 0x10) + 1) * 0x10) = param_3;
  }
  else {
    *(int *)(param_1 + *(int *)(param_1 + 0x418 + param_2 * 0x10) * 4) = param_3;
  }
  if (*(int *)(param_1 + 0x414 + param_3 * 0x10) == 0) {
    *(int *)(param_1 + 0x410 + *(int *)(param_1 + 0x418 + param_3 * 0x10) * 0x10) = param_2;
    *(int *)(param_1 + 0x410 + (*(int *)(param_1 + 0x418 + param_3 * 0x10) + 1) * 0x10) = param_2;
  }
  else {
    *(int *)(param_1 + *(int *)(param_1 + 0x418 + param_3 * 0x10) * 4) = param_2;
  }
  puVar1 = (undefined4 *)(param_1 + 0x40c + param_2 * 0x10);
  uVar3 = *puVar1;
  uVar4 = puVar1[1];
  uVar5 = puVar1[2];
  uVar6 = puVar1[3];
  puVar1 = (undefined4 *)(param_1 + 0x40c + param_3 * 0x10);
  puVar2 = (undefined4 *)(param_1 + 0x40c + param_2 * 0x10);
  *puVar2 = *puVar1;
  puVar2[1] = puVar1[1];
  puVar2[2] = puVar1[2];
  puVar2[3] = puVar1[3];
  *(undefined4 *)(param_1 + 0x410 + param_2 * 0x10) = uVar4;
  puVar1 = (undefined4 *)(param_1 + 0x40c + param_3 * 0x10);
  *puVar1 = uVar3;
  puVar1[1] = *(undefined4 *)(param_1 + 0x410 + param_3 * 0x10);
  puVar1[2] = uVar5;
  puVar1[3] = uVar6;
  return;
}

