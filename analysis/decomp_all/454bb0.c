
void FUN__text__00454bb0(int param_1,undefined4 param_2,undefined4 param_3)

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
  iVar1 = FUN__text__004551c0(param_2,param_3);
  if (iVar1 == 0) {
    if (param_1 == 1) {
      FUN__text__004549d0(0,param_2,param_3,1,0,0,1);
    }
  }
  else {
    FUN__text__004549d0(0,param_2,param_3,param_1,0,1,1);
  }
  local_8 = 0x454c33;
  FUN__text__0056ce80();
  return;
}

