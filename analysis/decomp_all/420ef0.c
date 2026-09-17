
void FUN__text__00420ef0(undefined4 param_1,undefined4 param_2,undefined2 param_3)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined4 *puVar4;
  undefined4 local_5c [16];
  void *local_1c;
  void *local_18;
  size_t local_14;
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  iVar3 = 0x16;
  puVar4 = local_5c;
  while( true ) {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__00420d80(CONCAT22(0xcccc,(undefined2)param_1));
  local_c = CONCAT22(local_c._2_2_,uVar2);
  uVar2 = FUN__text__00420d80(CONCAT22(extraout_var,(undefined2)param_2));
  local_10 = CONCAT22(local_10._2_2_,uVar2);
  local_14 = FUN__text__00420ba0(local_c & 0xffff,uVar2,CONCAT22(extraout_var_00,param_3));
  if ((local_14 == 0) &&
     (iVar3 = FUN__text__00424f80("size!=0","E:\\CrossHermit\\GAME\\src\\system\\Format.cpp",
                                  DAT_005ff5e8 + 10,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_1c = (void *)FUN__text__00428a40(local_14);
  local_18 = local_1c;
  if (local_1c != (void *)0x0) {
    _memset(local_1c,0,local_14);
    FUN__text__00420df0(param_1,param_2,local_c & 0xffff,local_10 & 0xffff,
                        CONCAT22(extraout_var_01,param_3),local_18);
  }
  local_8 = 0x420fe9;
  FUN__text__0056ce80();
  return;
}

