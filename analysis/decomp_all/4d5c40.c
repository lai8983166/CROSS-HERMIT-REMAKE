
void __thiscall FUN__text__004d5c40(int param_1,undefined4 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 4) = 0;
  local_8 = param_1;
  FUN__text__004d5bf0(param_3);
  FUN__text__004d5d10(param_2);
  local_8 = 0x4d5c8c;
  FUN__text__0056ce80();
  return;
}

