
void FUN__text__00419b30(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        )

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_4;
  iVar1 = FUN__text__00418f30(param_1,&DAT_005cbccc);
  if (iVar1 != 0) {
    FUN__text__00419e40(param_3,param_2);
    FUN__text__0042b2d0(&DAT_00592f50,param_3);
  }
  local_8 = 0x419b96;
  FUN__text__0056ce80();
  return;
}

