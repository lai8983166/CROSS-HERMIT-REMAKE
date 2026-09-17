
void FUN__text__00420ba0(undefined2 param_1,undefined2 param_2,uint param_3)

{
  code *pcVar1;
  undefined2 uVar2;
  ushort uVar3;
  int iVar4;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar5;
  undefined4 local_58 [16];
  uint local_18;
  ushort local_14;
  undefined2 uStack_12;
  uint local_10;
  int local_c;
  undefined4 local_8;
  
  iVar4 = 0x15;
  puVar5 = local_58;
  while( true ) {
    if (iVar4 == 0) break;
    iVar4 = iVar4 + -1;
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_18 = param_3 & 7;
  if (local_18 != 1) {
    if (local_18 == 2) {
      uVar2 = FUN__text__00420d80(param_1);
      local_10 = CONCAT22(local_10._2_2_,uVar2);
      uVar3 = FUN__text__00420d80(CONCAT22(extraout_var_00,param_2));
      _local_14 = CONCAT22(uStack_12,uVar3);
      local_c = (local_10 & 0xffff) * 2 * (uint)uVar3 + 0xc;
      goto LAB__text__00420c83;
    }
    iVar4 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\Format.cpp",
                                DAT_005ff5e0 + 6,0);
    if (iVar4 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uVar2 = FUN__text__00420d80(param_1);
  local_10 = CONCAT22(local_10._2_2_,uVar2);
  uVar3 = FUN__text__00420d80(CONCAT22(extraout_var,param_2));
  _local_14 = CONCAT22(uStack_12,uVar3);
  local_c = (local_10 & 0xffff) * (uint)uVar3 + 0x40c;
LAB__text__00420c83:
  local_8 = 0x420c93;
  FUN__text__0056ce80();
  return;
}

