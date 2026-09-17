
uint FUN__text1__0083ea4e(int *param_1,int param_2)

{
  undefined4 *puVar1;
  uint uVar2;
  int iVar3;
  uint local_14;
  uint local_10;
  
  if ((((param_1 == (int *)0x0) || (param_1[7] == 0)) || (4 < param_2)) || (param_2 < 0)) {
    uVar2 = 0xfffffffe;
  }
  else {
    puVar1 = (undefined4 *)param_1[7];
    if (((param_1[3] == 0) || ((*param_1 == 0 && (param_1[1] != 0)))) ||
       ((puVar1[1] == 0x29a && (param_2 != 4)))) {
      param_1[6] = (int)PTR_s_stream_error_0086ee3c;
      uVar2 = 0xfffffffe;
    }
    else if (param_1[4] == 0) {
      param_1[6] = (int)PTR_s_buffer_error_0086ee48;
      uVar2 = 0xfffffffb;
    }
    else {
      *puVar1 = param_1;
      iVar3 = puVar1[8];
      puVar1[8] = param_2;
      if (puVar1[1] == 0x2a) {
        local_14 = puVar1[0x1f] + -1 >> 1;
        if (3 < local_14) {
          local_14 = 3;
        }
        local_10 = ((puVar1[10] + -8) * 0x10 + 8) * 0x100 | local_14 << 6;
        if (puVar1[0x19] != 0) {
          local_10 = local_10 | 0x20;
        }
        puVar1[1] = 0x71;
        FUN__text1__0083edd0(puVar1,local_10 + (0x1f - local_10 % 0x1f));
        if (puVar1[0x19] != 0) {
          FUN__text1__0083edd0(puVar1,(uint)param_1[0xc] >> 0x10);
          FUN__text1__0083edd0(puVar1,param_1[0xc] & 0xffff);
        }
        param_1[0xc] = 1;
      }
      if (puVar1[5] == 0) {
        if (((param_1[1] == 0) && (param_2 <= iVar3)) && (param_2 != 4)) {
          param_1[6] = (int)PTR_s_buffer_error_0086ee48;
          return 0xfffffffb;
        }
      }
      else {
        FUN__text1__0083ee20(param_1);
        if (param_1[4] == 0) {
          puVar1[8] = 0xffffffff;
          return 0;
        }
      }
      if ((puVar1[1] == 0x29a) && (param_1[1] != 0)) {
        param_1[6] = (int)PTR_s_buffer_error_0086ee48;
        uVar2 = 0xfffffffb;
      }
      else {
        if (((param_1[1] != 0) || (puVar1[0x1b] != 0)) || ((param_2 != 0 && (puVar1[1] != 0x29a))))
        {
          iVar3 = (*(code *)(&PTR_DAT_00872e80)[puVar1[0x1f] * 3])(puVar1,param_2);
          if ((iVar3 == 2) || (iVar3 == 3)) {
            puVar1[1] = 0x29a;
          }
          if ((iVar3 == 0) || (iVar3 == 2)) {
            if (param_1[4] == 0) {
              puVar1[8] = 0xffffffff;
            }
            return 0;
          }
          if (iVar3 == 1) {
            if (param_2 == 1) {
              FUN__text1__00841aa3(puVar1);
            }
            else {
              FUN__text1__00841964(puVar1,0,0,0);
              if (param_2 == 3) {
                *(undefined2 *)(puVar1[0xf] + -2 + puVar1[0x11] * 2) = 0;
                _memset((void *)puVar1[0xf],0,puVar1[0x11] * 2 - 2);
              }
            }
            FUN__text1__0083ee20(param_1);
            if (param_1[4] == 0) {
              puVar1[8] = 0xffffffff;
              return 0;
            }
          }
        }
        if (param_2 == 4) {
          if (puVar1[6] == 0) {
            FUN__text1__0083edd0(puVar1,(uint)param_1[0xc] >> 0x10);
            FUN__text1__0083edd0(puVar1,param_1[0xc] & 0xffff);
            FUN__text1__0083ee20(param_1);
            puVar1[6] = 0xffffffff;
            uVar2 = (uint)(puVar1[5] == 0);
          }
          else {
            uVar2 = 1;
          }
        }
        else {
          uVar2 = 0;
        }
      }
    }
  }
  return uVar2;
}

