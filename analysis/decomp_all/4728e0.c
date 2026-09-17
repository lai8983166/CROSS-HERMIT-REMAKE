
void __thiscall FUN__text__004728e0(int param_1,undefined2 param_2,undefined2 param_3)

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
  *(undefined2 *)(param_1 + 0x10f9c0) = param_2;
  *(undefined2 *)(param_1 + 0x10f9c2) = param_3;
  local_8 = param_1;
  FUN__text__00409ff0(param_1 + 0x109dc8,1,0x58,0);
  *(undefined2 *)(local_8 + 0x109d8a) = 0;
  local_8 = 0x472950;
  FUN__text__0056ce80();
  return;
}

