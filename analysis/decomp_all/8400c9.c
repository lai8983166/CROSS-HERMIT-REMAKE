
uint FUN__text1__008400c9(int *param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  short sVar4;
  int iVar5;
  byte bVar6;
  ushort uVar7;
  int local_30;
  int local_2c;
  int local_28;
  uint local_24;
  uint local_c;
  
  local_c = 0;
  do {
    if ((uint)param_1[0x1b] < 0x106) {
      FUN__text1__0083f570(param_1);
      if (((uint)param_1[0x1b] < 0x106) && (param_2 == 0)) {
        return 0;
      }
      if (param_1[0x1b] == 0) {
        if (param_1[0x18] != 0) {
          bVar6 = *(byte *)(param_1[0xc] + -1 + param_1[0x19]);
          *(undefined2 *)(param_1[0x5a7] + param_1[0x5a6] * 2) = 0;
          *(byte *)(param_1[0x5a4] + param_1[0x5a6]) = bVar6;
          param_1[0x5a6] = param_1[0x5a6] + 1;
          *(short *)(param_1 + bVar6 + 0x23) = (short)param_1[bVar6 + 0x23] + 1;
          param_1[0x18] = 0;
        }
        if (param_1[0x15] < 0) {
          local_30 = 0;
        }
        else {
          local_30 = param_1[0xc] + param_1[0x15];
        }
        FUN__text1__00841f92(param_1,local_30,param_1[0x19] - param_1[0x15],param_2 == 4);
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
      uVar7 = *(ushort *)(param_1[0xf] + param_1[0x10] * 2);
      local_c = (uint)uVar7;
      *(ushort *)(param_1[0xe] + (param_1[0x19] & param_1[0xb]) * 2) = uVar7;
      *(short *)(param_1[0xf] + param_1[0x10] * 2) = (short)param_1[0x19];
    }
    param_1[0x1c] = param_1[0x16];
    param_1[0x17] = param_1[0x1a];
    param_1[0x16] = 2;
    if (((local_c != 0) && ((uint)param_1[0x1c] < (uint)param_1[0x1e])) &&
       (param_1[0x19] - local_c <= param_1[9] - 0x106U)) {
      if (param_1[0x20] != 2) {
        iVar5 = FUN__text1__0083fd9a(param_1,local_c);
        param_1[0x16] = iVar5;
      }
      if (((uint)param_1[0x16] < 6) &&
         ((param_1[0x20] == 1 ||
          ((param_1[0x16] == 3 && (0x1000 < (uint)(param_1[0x19] - param_1[0x1a]))))))) {
        param_1[0x16] = 2;
      }
    }
    if (((uint)param_1[0x1c] < 3) || ((uint)param_1[0x1c] < (uint)param_1[0x16])) {
      if (param_1[0x18] == 0) {
        param_1[0x18] = 1;
        param_1[0x19] = param_1[0x19] + 1;
        param_1[0x1b] = param_1[0x1b] + -1;
      }
      else {
        bVar6 = *(byte *)(param_1[0xc] + -1 + param_1[0x19]);
        *(undefined2 *)(param_1[0x5a7] + param_1[0x5a6] * 2) = 0;
        *(byte *)(param_1[0x5a4] + param_1[0x5a6]) = bVar6;
        param_1[0x5a6] = param_1[0x5a6] + 1;
        *(short *)(param_1 + bVar6 + 0x23) = (short)param_1[bVar6 + 0x23] + 1;
        if (param_1[0x5a6] == param_1[0x5a5] + -1) {
          if (param_1[0x15] < 0) {
            local_2c = 0;
          }
          else {
            local_2c = param_1[0xc] + param_1[0x15];
          }
          FUN__text1__00841f92(param_1,local_2c,param_1[0x19] - param_1[0x15],0);
          param_1[0x15] = param_1[0x19];
          FUN__text1__0083ee20(*param_1);
        }
        param_1[0x19] = param_1[0x19] + 1;
        param_1[0x1b] = param_1[0x1b] + -1;
        if (*(int *)(*param_1 + 0x10) == 0) {
          return 0;
        }
      }
    }
    else {
      iVar5 = param_1[0x19];
      iVar1 = param_1[0x1b];
      bVar6 = (char)param_1[0x1c] - 3;
      sVar4 = ((short)param_1[0x19] + -1) - (short)param_1[0x17];
      *(short *)(param_1[0x5a7] + param_1[0x5a6] * 2) = sVar4;
      *(byte *)(param_1[0x5a4] + param_1[0x5a6]) = bVar6;
      param_1[0x5a6] = param_1[0x5a6] + 1;
      uVar7 = sVar4 - 1;
      *(short *)(param_1 + (byte)(&DAT_00873b38)[bVar6] + 0x124) =
           (short)param_1[(byte)(&DAT_00873b38)[bVar6] + 0x124] + 1;
      if (uVar7 < 0x100) {
        bVar6 = (&DAT_00873938)[uVar7];
      }
      else {
        bVar6 = (&DAT_00873a38)[(int)(uint)uVar7 >> 7];
      }
      local_24 = (uint)bVar6;
      *(short *)(param_1 + local_24 + 0x260) = (short)param_1[local_24 + 0x260] + 1;
      iVar2 = param_1[0x5a5];
      iVar3 = param_1[0x5a6];
      param_1[0x1b] = param_1[0x1b] - (param_1[0x1c] + -1);
      param_1[0x1c] = param_1[0x1c] + -2;
      do {
        param_1[0x19] = param_1[0x19] + 1;
        if ((uint)param_1[0x19] <= (uint)(iVar5 + -3 + iVar1)) {
          param_1[0x10] =
               (param_1[0x10] << ((byte)param_1[0x14] & 0x1f) ^
               (uint)*(byte *)(param_1[0xc] + 2 + param_1[0x19])) & param_1[0x13];
          uVar7 = *(ushort *)(param_1[0xf] + param_1[0x10] * 2);
          local_c = (uint)uVar7;
          *(ushort *)(param_1[0xe] + (param_1[0x19] & param_1[0xb]) * 2) = uVar7;
          *(short *)(param_1[0xf] + param_1[0x10] * 2) = (short)param_1[0x19];
        }
        param_1[0x1c] = param_1[0x1c] + -1;
      } while (param_1[0x1c] != 0);
      param_1[0x18] = 0;
      param_1[0x16] = 2;
      param_1[0x19] = param_1[0x19] + 1;
      if (iVar3 == iVar2 + -1) {
        if (param_1[0x15] < 0) {
          local_28 = 0;
        }
        else {
          local_28 = param_1[0xc] + param_1[0x15];
        }
        FUN__text1__00841f92(param_1,local_28,param_1[0x19] - param_1[0x15],0);
        param_1[0x15] = param_1[0x19];
        FUN__text1__0083ee20(*param_1);
        if (*(int *)(*param_1 + 0x10) == 0) {
          return 0;
        }
      }
    }
  } while( true );
}

