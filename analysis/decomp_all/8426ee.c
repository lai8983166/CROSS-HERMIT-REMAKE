
void FUN__text1__008426ee(int param_1,int param_2,int param_3)

{
  int iVar1;
  int local_c;
  
  iVar1 = *(int *)(param_1 + 0xb54 + param_3 * 4);
  while (local_c = param_3 * 2, local_c <= *(int *)(param_1 + 0x1448)) {
    if ((local_c < *(int *)(param_1 + 0x1448)) &&
       ((*(ushort *)(param_2 + *(int *)(param_1 + 0xb58 + param_3 * 8) * 4) <
         *(ushort *)(param_2 + *(int *)(param_1 + 0xb54 + param_3 * 8) * 4) ||
        ((*(short *)(param_2 + *(int *)(param_1 + 0xb58 + param_3 * 8) * 4) ==
          *(short *)(param_2 + *(int *)(param_1 + 0xb54 + param_3 * 8) * 4) &&
         (*(byte *)(param_1 + 0x1450 + *(int *)(param_1 + 0xb58 + param_3 * 8)) <=
          *(byte *)(param_1 + 0x1450 + *(int *)(param_1 + 0xb54 + param_3 * 8)))))))) {
      local_c = local_c + 1;
    }
    if ((*(ushort *)(param_2 + iVar1 * 4) <
         *(ushort *)(param_2 + *(int *)(param_1 + 0xb54 + local_c * 4) * 4)) ||
       ((*(short *)(param_2 + iVar1 * 4) ==
         *(short *)(param_2 + *(int *)(param_1 + 0xb54 + local_c * 4) * 4) &&
        (*(byte *)(param_1 + iVar1 + 0x1450) <=
         *(byte *)(param_1 + 0x1450 + *(int *)(param_1 + 0xb54 + local_c * 4)))))) break;
    *(undefined4 *)(param_1 + 0xb54 + param_3 * 4) = *(undefined4 *)(param_1 + 0xb54 + local_c * 4);
    param_3 = local_c;
  }
  *(int *)(param_1 + 0xb54 + param_3 * 4) = iVar1;
  return;
}

