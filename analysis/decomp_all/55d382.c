
void FUN__text__0055d382(int param_1,undefined4 *param_2,uint param_3)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  
  puVar3 = *(undefined4 **)(param_1 + 0x28);
  for (uVar1 = param_3 >> 2; uVar1 != 0; uVar1 = uVar1 - 1) {
    *puVar3 = *param_2;
    param_2 = param_2 + 1;
    puVar3 = puVar3 + 1;
  }
  for (uVar1 = param_3 & 3; uVar1 != 0; uVar1 = uVar1 - 1) {
    *(undefined1 *)puVar3 = *(undefined1 *)param_2;
    param_2 = (undefined4 *)((int)param_2 + 1);
    puVar3 = (undefined4 *)((int)puVar3 + 1);
  }
  iVar2 = *(int *)(param_1 + 0x28) + param_3;
  *(int *)(param_1 + 0x34) = iVar2;
  *(int *)(param_1 + 0x30) = iVar2;
  return;
}

