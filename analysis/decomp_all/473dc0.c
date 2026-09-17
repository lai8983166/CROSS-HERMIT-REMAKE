
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00473dc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  short local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if ((iVar1 != 0) && (iVar1 = FUN__text__004daae0((int)DAT_007f4488), iVar1 != 0)) {
    if (param_1 == 0) {
      _memset(&DAT_007f4518,0,0x3700);
      local_10 = 0;
      for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
        local_18 = local_8 + 0x80aec + local_c * 0x520;
        iVar1 = FUN__text__00468d10(local_18);
        if ((iVar1 != 0) && (iVar1 = FUN__text__0046a4c0(local_18), iVar1 != 0)) {
          puVar2 = *(undefined4 **)(local_8 + 0x80d44 + local_c * 0x520);
          puVar3 = (undefined4 *)(&DAT_007f4518 + local_10 * 0xb0);
          for (iVar1 = 0x2c; iVar1 != 0; iVar1 = iVar1 + -1) {
            *puVar3 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar3 = puVar3 + 1;
          }
          local_10 = local_10 + 1;
        }
      }
      DAT_007f448c._1_1_ = (char)local_10;
    }
    else {
      for (local_c = 0; local_c != 0x50; local_c = local_c + 1) {
        *(undefined2 *)(&DAT_008093fa + local_c * 8) =
             *(undefined2 *)(&DAT_007f45c0 + local_c * 0xb0);
        *(undefined2 *)(&DAT_008093fc + local_c * 8) =
             *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0);
        *(undefined2 *)(&DAT_008093fe + local_c * 8) =
             *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0);
        (&DAT_00809400)[local_c * 8] = (&DAT_007f45c6)[local_c * 0xb0];
      }
      _memset(&DAT_007f4518,0,0x3700);
      local_10 = 0;
      for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
        local_18 = local_8 + 0x80aec + local_c * 0x520;
        iVar1 = FUN__text__00468d10(local_18);
        if ((iVar1 != 0) && (iVar1 = FUN__text__0046a4c0(local_18), iVar1 != 0)) {
          puVar2 = *(undefined4 **)(local_8 + 0x80d44 + local_c * 0x520);
          puVar3 = (undefined4 *)(&DAT_007f4518 + local_10 * 0xb0);
          for (iVar1 = 0x2c; iVar1 != 0; iVar1 = iVar1 + -1) {
            *puVar3 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar3 = puVar3 + 1;
          }
          *(undefined2 *)(&DAT_007f45c0 + local_10 * 0xb0) =
               *(undefined2 *)(&DAT_008093fa + local_c * 8);
          *(undefined2 *)(&DAT_007f45c2 + local_10 * 0xb0) =
               *(undefined2 *)(&DAT_008093fc + local_c * 8);
          *(undefined2 *)(&DAT_007f45c4 + local_10 * 0xb0) =
               *(undefined2 *)(&DAT_008093fe + local_c * 8);
          (&DAT_007f45c6)[local_10 * 0xb0] = (&DAT_00809400)[local_c * 8];
          local_10 = local_10 + 1;
        }
      }
      DAT_007f448c._1_1_ = (char)local_10;
    }
    DAT_007a5296 = 1;
    DAT_007a5298 = 1;
    _DAT_007a52f8 = (short)DAT_007f448c._1_1_;
    _memset(&DAT_007a52d0,0,0x28);
    for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      *(undefined2 *)(&DAT_007a52d0 + local_c * 2) = *(undefined2 *)(&DAT_007f451a + local_c * 0xb0)
      ;
    }
    if ((DAT_007f4488 < 0x25) || (0x28 < DAT_007f4488)) {
      if ((DAT_007f4488 < 0x30) || (0x44 < DAT_007f4488)) {
        local_1c = (int)DAT_007f4488;
        if ((local_1c < 0x96) || (0x9a < local_1c)) {
          local_14 = 0x25;
        }
        else {
          local_14 = DAT_007f4488;
        }
      }
      else {
        local_14 = 0x30;
      }
    }
    else {
      local_14 = 0x25;
    }
    DAT_007a5294 = local_14;
  }
  local_8 = 0x474164;
  FUN__text__0056ce80();
  return;
}

