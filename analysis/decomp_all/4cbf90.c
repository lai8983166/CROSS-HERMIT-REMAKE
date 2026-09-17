
void FUN__text__004cbf90(int param_1)

{
  ushort uVar1;
  undefined1 uVar2;
  undefined2 extraout_var;
  int iVar3;
  undefined2 extraout_var_00;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  uint local_20;
  undefined **local_1c;
  undefined **local_18;
  ushort local_14;
  undefined2 uStack_12;
  undefined2 local_10;
  undefined1 local_c;
  uint local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__004ca9b0();
  local_8 = CONCAT31(local_8._1_3_,uVar2);
  local_c = FUN__text__004ca9e0();
  local_10 = *(undefined2 *)(param_1 + 0x40 + (local_8 & 0xff) * 2);
  uVar1 = *(ushort *)(param_1 + 0x34 + (local_8 & 0xff) * 2);
  _local_14 = CONCAT22(uStack_12,uVar1);
  local_20 = (uint)*(ushort *)(param_1 + 0x30);
  if (local_20 == 0) {
    local_1c = &PTR_s_sc000_bin_00622668 + (uint)uVar1 * 0xf;
    *(undefined ***)(param_1 + 0x44 + (local_8 & 0xff) * 4) = local_1c;
    FUN__text__004cd7b0("data\\adv\\bin\\",&DAT_007a4d4c);
    FUN__text__004cd810(&DAT_007a4d4c,*local_1c);
    FUN__text__004cde10(&DAT_007a4d4c,CONCAT22(extraout_var_00,local_10));
  }
  else if (local_20 == 1) {
    local_18 = &PTR_s_mc000_bin_00622250 + (uint)uVar1 * 2;
    *(undefined ***)(param_1 + 0x44 + (local_8 & 0xff) * 4) = local_18;
    FUN__text__004cd7b0("data\\adv\\bin\\",&DAT_007a4c84);
    FUN__text__004cd810(&DAT_007a4c84,*local_18);
    FUN__text__004cde10(&DAT_007a4c84,CONCAT22(extraout_var,local_10));
  }
  local_8 = 0x4cc0e5;
  FUN__text__0056ce80();
  return;
}

