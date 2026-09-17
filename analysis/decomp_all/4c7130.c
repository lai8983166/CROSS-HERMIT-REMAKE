
void __fastcall FUN__text__004c7130(int param_1)

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
  *(undefined1 *)(param_1 + 8) = 0;
  *(undefined2 *)(param_1 + 10) = 0;
  *(undefined2 *)(param_1 + 0xe) = 0xffff;
  *(undefined2 *)(param_1 + 0x10) = 0xffff;
  local_8 = param_1;
  FUN__text__004c6da0();
  local_8 = 0x4c7186;
  FUN__text__0056ce80();
  return;
}

