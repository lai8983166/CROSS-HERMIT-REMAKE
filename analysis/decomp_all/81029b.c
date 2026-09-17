
void FUN__text1__0081029b(int param_1,int param_2)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  
  iVar4 = *(int *)(param_1 + 0x408) + -1;
  iVar3 = *(int *)(param_1 + 0x408);
  iVar5 = *(int *)(param_1 + 0x408) + 1;
  *(int *)(param_1 + 0x408) = *(int *)(param_1 + 0x408) + 2;
  puVar1 = (undefined4 *)(param_1 + 0x40c + iVar4 * 0x10);
  puVar2 = (undefined4 *)(param_1 + 0x40c + iVar3 * 0x10);
  *puVar2 = *puVar1;
  puVar2[1] = puVar1[1];
  puVar2[2] = puVar1[2];
  puVar2[3] = puVar1[3];
  *(int *)(param_1 + 0x410 + iVar3 * 0x10) = iVar4;
  *(int *)(param_1 + *(int *)(param_1 + 0x418 + iVar3 * 0x10) * 4) = iVar3;
  *(int *)(param_1 + 0x418 + iVar4 * 0x10) = iVar3;
  *(undefined4 *)(param_1 + 0x414 + iVar4 * 0x10) = 0;
  *(int *)(param_1 + 0x418 + iVar5 * 0x10) = param_2;
  *(undefined4 *)(param_1 + 0x414 + iVar5 * 0x10) = 1;
  *(undefined4 *)(param_1 + 0x40c + iVar5 * 0x10) = 0;
  *(int *)(param_1 + 0x410 + iVar5 * 0x10) = iVar4;
  *(int *)(param_1 + param_2 * 4) = iVar5;
  return;
}

