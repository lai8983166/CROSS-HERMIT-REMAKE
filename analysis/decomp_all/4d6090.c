
void __thiscall FUN__text__004d6090(undefined4 *param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = param_2;
  local_8 = param_1;
  FUN__text__004d60e0(param_3);
  local_8 = (undefined4 *)0x4d60ce;
  FUN__text__0056ce80();
  return;
}

