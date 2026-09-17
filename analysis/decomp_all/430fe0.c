
void __thiscall FUN__text__00430fe0(int param_1,short *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_10 = 0; local_10 != 5; local_10 = local_10 + 1) {
    param_2[local_10] = 0;
    param_2[local_10 + 5] = 0;
    param_2[local_10 + 10] = 0;
    param_2[local_10 + 0xf] = 0;
    param_2[local_10 + 0x14] = 0;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 0xfa; local_10 = local_10 + 1) {
    local_c = local_8 + 0x80aec + local_10 * 0x520;
    iVar1 = FUN__text__00468d10(local_c);
    if (iVar1 != 0) {
      iVar1 = FUN__text__00469ad0(local_c);
      if (iVar1 != 0) {
        iVar1 = FUN__text__00469eb0(local_c);
        if (iVar1 != 0) {
          iVar1 = FUN__text__0046a430(local_c);
          if ((iVar1 == 0) && (iVar1 = FUN__text__0046a5e0(local_c), iVar1 == 0)) {
            iVar1 = FUN__text__00469220(local_c);
            if (iVar1 == 0) {
              param_2[1] = param_2[1] + 1;
            }
            else {
              param_2[3] = param_2[3] + 1;
            }
          }
          else {
            iVar1 = FUN__text__00469220(local_c);
            if (iVar1 == 0) {
              *param_2 = *param_2 + 1;
            }
            else {
              param_2[2] = param_2[2] + 1;
            }
          }
          param_2[4] = param_2[4] + 1;
        }
        iVar1 = FUN__text__00469f90(local_c);
        if (iVar1 != 0) {
          iVar1 = FUN__text__0046a430(local_c);
          if ((iVar1 == 0) && (iVar1 = FUN__text__0046a5e0(local_c), iVar1 == 0)) {
            iVar1 = FUN__text__00469220(local_c);
            if (iVar1 == 0) {
              param_2[6] = param_2[6] + 1;
            }
            else {
              param_2[8] = param_2[8] + 1;
            }
          }
          else {
            iVar1 = FUN__text__00469220(local_c);
            if (iVar1 == 0) {
              param_2[5] = param_2[5] + 1;
            }
            else {
              param_2[7] = param_2[7] + 1;
            }
          }
          param_2[9] = param_2[9] + 1;
        }
        param_2[0xe] = param_2[0xe] + 1;
      }
      iVar1 = FUN__text__00469c60(local_c);
      if (iVar1 != 0) {
        iVar1 = FUN__text__0046a430(local_c);
        if ((iVar1 == 0) && (iVar1 = FUN__text__0046a5e0(local_c), iVar1 == 0)) {
          iVar1 = FUN__text__00469220(local_c);
          if (iVar1 == 0) {
            param_2[0x10] = param_2[0x10] + 1;
          }
          else {
            param_2[0x12] = param_2[0x12] + 1;
          }
        }
        else {
          iVar1 = FUN__text__00469220(local_c);
          if (iVar1 == 0) {
            param_2[0xf] = param_2[0xf] + 1;
          }
          else {
            param_2[0x11] = param_2[0x11] + 1;
          }
        }
        param_2[0x13] = param_2[0x13] + 1;
      }
      iVar1 = FUN__text__00469b90(local_c);
      if (iVar1 != 0) {
        iVar1 = FUN__text__0046a430(local_c);
        if ((iVar1 == 0) && (iVar1 = FUN__text__0046a5e0(local_c), iVar1 == 0)) {
          iVar1 = FUN__text__00469220(local_c);
          if (iVar1 == 0) {
            param_2[0x15] = param_2[0x15] + 1;
          }
          else {
            param_2[0x17] = param_2[0x17] + 1;
          }
        }
        else {
          iVar1 = FUN__text__00469220(local_c);
          if (iVar1 == 0) {
            param_2[0x14] = param_2[0x14] + 1;
          }
          else {
            param_2[0x16] = param_2[0x16] + 1;
          }
        }
        param_2[0x18] = param_2[0x18] + 1;
      }
    }
  }
  for (local_10 = 0; local_10 != 5; local_10 = local_10 + 1) {
    param_2[local_10 + 10] = param_2[local_10] + param_2[local_10 + 5];
  }
  local_8 = 0x4313e2;
  FUN__text__0056ce80();
  return;
}

