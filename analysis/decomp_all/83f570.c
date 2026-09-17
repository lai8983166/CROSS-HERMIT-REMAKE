
void FUN__text1__0083f570(int *param_1)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  ushort local_20;
  ushort local_1c;
  uint local_18;
  uint local_10;
  ushort *local_c;
  
  uVar1 = param_1[9];
  while( true ) {
    uVar3 = (param_1[0xd] - param_1[0x1b]) - param_1[0x19];
    if (((uVar3 != 0) || (param_1[0x19] != 0)) || (local_10 = uVar1, param_1[0x1b] != 0)) {
      if (uVar3 == 0xffffffff) {
        local_10 = 0xfffffffe;
      }
      else {
        local_10 = uVar3;
        if ((uVar1 - 0x106) + param_1[9] <= (uint)param_1[0x19]) {
          FUN__text1__00848490(param_1[0xc],param_1[0xc] + uVar1,uVar1);
          param_1[0x1a] = param_1[0x1a] - uVar1;
          param_1[0x19] = param_1[0x19] - uVar1;
          param_1[0x15] = param_1[0x15] - uVar1;
          local_18 = param_1[0x11];
          local_c = (ushort *)(param_1[0xf] + local_18 * 2);
          do {
            local_c = local_c + -1;
            if (*local_c < uVar1) {
              local_1c = 0;
            }
            else {
              local_1c = *local_c - (short)uVar1;
            }
            *local_c = local_1c;
            local_18 = local_18 + -1;
          } while (local_18 != 0);
          local_c = (ushort *)(param_1[0xe] + uVar1 * 2);
          local_18 = uVar1;
          do {
            local_c = local_c + -1;
            if (*local_c < uVar1) {
              local_20 = 0;
            }
            else {
              local_20 = *local_c - (short)uVar1;
            }
            *local_c = local_20;
            local_18 = local_18 - 1;
          } while (local_18 != 0);
          local_10 = uVar3 + uVar1;
        }
      }
    }
    if (*(int *)(*param_1 + 4) == 0) break;
    iVar2 = FUN__text1__0083f7ab(*param_1,param_1[0xc] + param_1[0x19] + param_1[0x1b],local_10);
    param_1[0x1b] = param_1[0x1b] + iVar2;
    if (2 < (uint)param_1[0x1b]) {
      param_1[0x10] = (uint)*(byte *)(param_1[0xc] + param_1[0x19]);
      param_1[0x10] =
           (param_1[0x10] << ((byte)param_1[0x14] & 0x1f) ^
           (uint)*(byte *)(param_1[0xc] + 1 + param_1[0x19])) & param_1[0x13];
    }
    if (0x105 < (uint)param_1[0x1b]) {
      return;
    }
    if (*(int *)(*param_1 + 4) == 0) {
      return;
    }
  }
  return;
}

