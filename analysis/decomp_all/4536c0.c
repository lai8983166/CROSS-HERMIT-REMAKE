
void __fastcall FUN__text__004536c0(int param_1)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  undefined1 local_20;
  char local_1c;
  uint local_18;
  int local_14;
  int local_10;
  undefined4 *local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  for (local_10 = 0; local_10 != DAT_007f448c._1_1_; local_10 = local_10 + 1) {
    if (*(char *)(*(int *)(param_1 + 0x80ed4 + local_10 * 0x520) + 0xf) == '\x01') {
      local_14 = local_14 + 1;
    }
  }
  local_18 = (uint)(local_14 == 0);
  if (((local_18 == 0) && (*(int *)(param_1 + 0x2e884) != 0)) &&
     ((local_8 = param_1, iVar1 = FUN__text__00456b20(), iVar1 == 0 ||
      ((iVar1 = FUN__text__004daae0((int)DAT_007f4488), iVar1 == 0 ||
       (iVar1 = FUN__text__00430f60(), iVar1 == 0)))))) {
    FUN__text__004dab50();
    for (local_10 = 0; local_10 != DAT_007f448c._1_1_; local_10 = local_10 + 1) {
      iVar1 = local_10 * 0xb0;
      local_c = (undefined4 *)(&DAT_007f4518 + iVar1);
      puVar3 = (undefined4 *)(local_8 + 0xd0dbc + local_10 * 0xb0);
      puVar4 = local_c;
      for (iVar2 = 0x2c; iVar2 != 0; iVar2 = iVar2 + -1) {
        *puVar4 = *puVar3;
        puVar3 = puVar3 + 1;
        puVar4 = puVar4 + 1;
      }
      (&DAT_007f45b5)[iVar1] = 0;
      (&DAT_007f45b6)[iVar1] = 0;
      (&DAT_007f45b7)[iVar1] = 2;
      (&DAT_007f45b8)[iVar1] = 0;
      (&DAT_007f45b9)[iVar1] = 0;
      (&DAT_007f45ba)[iVar1] = 0;
      (&DAT_007f45bb)[iVar1] = 0;
    }
    local_1c = DAT_007f448c._1_1_;
    local_20 = DAT_007f4491;
    DAT_007f4488 = DAT_007f448a;
    FUN__text__004da8a0((int)DAT_007f448a,0);
    DAT_007f448c._0_1_ = 1;
    DAT_007f448c._1_1_ = local_1c;
    DAT_007f4491 = local_20;
  }
  local_8 = 0x453885;
  FUN__text__0056ce80();
  return;
}

