
void FUN__text__004902e0(undefined4 param_1,undefined1 *param_2,int param_3)

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
  *param_2 = 0;
  _memset(param_2,0,0x10);
  FUN__text__0046beb0(param_1,0xffffffff,0,0,param_3 + 2,0);
  local_8 = 0x49033b;
  FUN__text__0056ce80();
  return;
}

