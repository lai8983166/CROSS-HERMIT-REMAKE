
void __thiscall
FUN__text__004d5ca0(undefined2 *param_1,undefined4 param_2,undefined2 param_3,undefined2 param_4,
                   undefined2 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined2 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = param_4;
  param_1[1] = param_5;
  param_1[2] = 0;
  local_8 = param_1;
  FUN__text__004d5bf0(param_3);
  FUN__text__004d5d10(param_2);
  local_8 = (undefined2 *)0x4d5d01;
  FUN__text__0056ce80();
  return;
}

