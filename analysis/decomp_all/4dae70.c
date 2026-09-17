
void FUN__text__004dae70(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined *local_10;
  undefined *local_c;
  undefined *local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = &DAT_008093fa;
  local_c = &DAT_0080967a;
  local_10 = &DAT_007f4518;
  for (local_14 = 0; local_14 != DAT_007f448c._1_1_; local_14 = local_14 + 1) {
    *(undefined2 *)(&DAT_007f45c0 + local_14 * 0xb0) = *(undefined2 *)(&DAT_008093fa + local_14 * 8)
    ;
    *(undefined2 *)(&DAT_007f45c2 + local_14 * 0xb0) = *(undefined2 *)(&DAT_008093fc + local_14 * 8)
    ;
    *(undefined2 *)(&DAT_007f45c4 + local_14 * 0xb0) = *(undefined2 *)(&DAT_008093fe + local_14 * 8)
    ;
    (&DAT_007f45c6)[local_14 * 0xb0] = (&DAT_00809400)[local_14 * 8];
  }
  local_18 = (int)DAT_0080968a / (int)DAT_008093f8;
  if (local_18 < 10) {
    if (local_18 < 7) {
      if (local_18 < 5) {
        if (local_18 < 1) {
          DAT_007f450c = 5;
        }
        else {
          DAT_007f450c = 4;
        }
      }
      else {
        DAT_007f450c = 3;
      }
    }
    else {
      DAT_007f450c = 2;
    }
  }
  else {
    DAT_007f450c = 1;
  }
  DAT_007f450e = DAT_0080968c;
  DAT_007f4510 = DAT_0080968e;
  DAT_007f4512 = DAT_00809690;
  _memset(&DAT_007f44be,0,0x10);
  for (local_14 = 0; local_14 != 0x10; local_14 = local_14 + 1) {
    (&DAT_007f44be)[local_14] = local_c[local_14];
  }
  local_8 = (undefined *)0x4db00c;
  FUN__text__0056ce80();
  return;
}

