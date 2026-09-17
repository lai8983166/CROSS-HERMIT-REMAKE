
uint FUN__text1__0083f843(int *param_1,int param_2)

{
  int iVar1;
  byte bVar2;
  short sVar3;
  ushort uVar4;
  bool bVar5;
  int local_24;
  int local_20;
  uint local_1c;
  uint local_c;
  
  local_c = 0;
  do {
    if ((uint)param_1[0x1b] < 0x106) {
      FUN__text1__0083f570(param_1);
      if (((uint)param_1[0x1b] < 0x106) && (param_2 == 0)) {
        return 0;
      }
      if (param_1[0x1b] == 0) {
        if (param_1[0x15] < 0) {
          local_24 = 0;
        }
        else {
          local_24 = param_1[0xc] + param_1[0x15];
        }
        FUN__text1__00841f92(param_1,local_24,param_1[0x19] - param_1[0x15],param_2 == 4);
        param_1[0x15] = param_1[0x19];
        FUN__text1__0083ee20(*param_1);
        if (*(int *)(*param_1 + 0x10) == 0) {
          return (param_2 != 4) - 1 & 2;
        }
        return (-(uint)(param_2 != 4) & 0xfffffffe) + 3;
      }
    }
    if (2 < (uint)param_1[0x1b]) {
      param_1[0x10] =
           (param_1[0x10] << ((byte)param_1[0x14] & 0x1f) ^
           (uint)*(byte *)(param_1[0xc] + 2 + param_1[0x19])) & param_1[0x13];
      uVar4 = *(ushort *)(param_1[0xf] + param_1[0x10] * 2);
      local_c = (uint)uVar4;
      *(ushort *)(param_1[0xe] + (param_1[0x19] & param_1[0xb]) * 2) = uVar4;
      *(short *)(param_1[0xf] + param_1[0x10] * 2) = (short)param_1[0x19];
    }
    if (((local_c != 0) && (param_1[0x19] - local_c <= param_1[9] - 0x106U)) && (param_1[0x20] != 2)
       ) {
      iVar1 = FUN__text1__0083fd9a(param_1,local_c);
      param_1[0x16] = iVar1;
    }
    if ((uint)param_1[0x16] < 3) {
      bVar2 = *(byte *)(param_1[0xc] + param_1[0x19]);
      *(undefined2 *)(param_1[0x5a7] + param_1[0x5a6] * 2) = 0;
      *(byte *)(param_1[0x5a4] + param_1[0x5a6]) = bVar2;
      param_1[0x5a6] = param_1[0x5a6] + 1;
      *(short *)(param_1 + bVar2 + 0x23) = (short)param_1[bVar2 + 0x23] + 1;
      bVar5 = param_1[0x5a6] == param_1[0x5a5] + -1;
      param_1[0x1b] = param_1[0x1b] + -1;
      param_1[0x19] = param_1[0x19] + 1;
    }
    else {
      bVar2 = (char)param_1[0x16] - 3;
      sVar3 = (short)param_1[0x19] - (short)param_1[0x1a];
      *(short *)(param_1[0x5a7] + param_1[0x5a6] * 2) = sVar3;
      *(byte *)(param_1[0x5a4] + param_1[0x5a6]) = bVar2;
      param_1[0x5a6] = param_1[0x5a6] + 1;
      uVar4 = sVar3 - 1;
      *(short *)(param_1 + (byte)(&DAT_00873b38)[bVar2] + 0x124) =
           (short)param_1[(byte)(&DAT_00873b38)[bVar2] + 0x124] + 1;
      if (uVar4 < 0x100) {
        bVar2 = (&DAT_00873938)[uVar4];
      }
      else {
        bVar2 = (&DAT_00873a38)[(int)(uint)uVar4 >> 7];
      }
      local_1c = (uint)bVar2;
      *(short *)(param_1 + local_1c + 0x260) = (short)param_1[local_1c + 0x260] + 1;
      bVar5 = param_1[0x5a6] == param_1[0x5a5] + -1;
      param_1[0x1b] = param_1[0x1b] - param_1[0x16];
      if (((uint)param_1[0x1e] < (uint)param_1[0x16]) || ((uint)param_1[0x1b] < 3)) {
        param_1[0x19] = param_1[0x19] + param_1[0x16];
        param_1[0x16] = 0;
        param_1[0x10] = (uint)*(byte *)(param_1[0xc] + param_1[0x19]);
        param_1[0x10] =
             (param_1[0x10] << ((byte)param_1[0x14] & 0x1f) ^
             (uint)*(byte *)(param_1[0xc] + 1 + param_1[0x19])) & param_1[0x13];
      }
      else {
        param_1[0x16] = param_1[0x16] + -1;
        do {
          param_1[0x19] = param_1[0x19] + 1;
          param_1[0x10] =
               (param_1[0x10] << ((byte)param_1[0x14] & 0x1f) ^
               (uint)*(byte *)(param_1[0xc] + 2 + param_1[0x19])) & param_1[0x13];
          uVar4 = *(ushort *)(param_1[0xf] + param_1[0x10] * 2);
          local_c = (uint)uVar4;
          *(ushort *)(param_1[0xe] + (param_1[0x19] & param_1[0xb]) * 2) = uVar4;
          *(short *)(param_1[0xf] + param_1[0x10] * 2) = (short)param_1[0x19];
          param_1[0x16] = param_1[0x16] + -1;
        } while (param_1[0x16] != 0);
        param_1[0x19] = param_1[0x19] + 1;
      }
    }
    if (bVar5) {
      if (param_1[0x15] < 0) {
        local_20 = 0;
      }
      else {
        local_20 = param_1[0xc] + param_1[0x15];
      }
      FUN__text1__00841f92(param_1,local_20,param_1[0x19] - param_1[0x15],0);
      param_1[0x15] = param_1[0x19];
      FUN__text1__0083ee20(*param_1);
      if (*(int *)(*param_1 + 0x10) == 0) {
        return 0;
      }
    }
  } while( true );
}

