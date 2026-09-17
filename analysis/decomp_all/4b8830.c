
void FUN__text__004b8830(undefined2 param_1,undefined2 param_2,undefined1 param_3,undefined2 param_4
                        ,undefined2 param_5)

{
  uint uVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = FUN__text__004d1ba0(param_3,0,6);
  FUN__text__004d2790(&DAT_0061bf20,1,param_4,CONCAT22(extraout_var,param_1),param_2,
                      (uVar1 & 0xff) * 0x16,CONCAT22(extraout_var,param_5));
  local_8 = 0x4b88ab;
  FUN__text__0056ce80();
  return;
}

