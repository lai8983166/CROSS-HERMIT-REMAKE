
void FUN__text__00405a80(int param_1,int *param_2,int param_3,undefined4 param_4,int *param_5,
                        int *param_6)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_68 [20];
  int local_18;
  int local_14;
  
  puVar5 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  for (local_18 = 0; local_18 != param_5[3]; local_18 = local_18 + 1) {
    iVar3 = *param_5;
    iVar1 = param_5[1];
    iVar4 = param_2[1] + *param_6 * 2 + (param_6[1] + local_18) * *param_2;
    for (local_14 = 0; local_14 != param_5[2]; local_14 = local_14 + 1) {
      uVar2 = *(uint *)(param_1 + iVar3 * 4 + (iVar1 + local_18) * 4 * param_3 + local_14 * 4);
      if ((uVar2 & 0xffffff) == 0) {
        *(undefined2 *)(iVar4 + local_14 * 2) = 0;
      }
      else {
        *(ushort *)(iVar4 + local_14 * 2) =
             (ushort)((uVar2 & 0xf80000) >> 9) | 0x8000 | (ushort)((uVar2 & 0xf800) >> 6) |
             (ushort)((uVar2 & 0xf8) >> 3);
      }
    }
  }
  return;
}

