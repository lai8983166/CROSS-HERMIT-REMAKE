
undefined4 FUN__text1__00834c73(int param_1,int param_2,ushort *param_3,int param_4)

{
  ushort uVar1;
  int iVar2;
  int iVar3;
  uint local_2c;
  uint local_28;
  ushort *local_18;
  ushort *local_c;
  
  local_c = param_3;
  param_3 = (ushort *)((int)param_3 + param_4);
  param_2 = param_1 - param_2;
  if (param_2 != 0) {
    while (local_c < param_3) {
      iVar2 = *(int *)local_c;
      local_18 = (ushort *)((int)local_c + *(int *)(local_c + 2));
      if (param_3 < (ushort *)((int)local_c + *(int *)(local_c + 2))) {
        local_18 = param_3;
      }
      local_c = local_c + 4;
      iVar2 = iVar2 + param_1;
      while (local_c < local_18) {
        uVar1 = *local_c;
        local_2c = (uint)uVar1;
        local_c = local_c + 1;
        iVar3 = (int)(local_2c & 0xf000) >> 0xc;
        local_28 = (uint)(uVar1 & 0xfff);
        if (iVar3 == 1) {
          *(undefined2 *)(iVar2 + local_28) = *(undefined2 *)(iVar2 + local_28);
        }
        else if (iVar3 == 2) {
          *(short *)(iVar2 + local_28) = *(short *)(iVar2 + local_28) + ((ushort)param_2 & 0xff);
        }
        else if (iVar3 == 3) {
          *(int *)(iVar2 + local_28) = *(int *)(iVar2 + local_28) + param_2;
        }
        else if (iVar3 != 0) {
          return 0;
        }
      }
    }
  }
  return 1;
}

