
void __thiscall
FUN__text__004143a0(int param_1,undefined1 param_2,undefined1 param_3,undefined1 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_1 + 0xb276) = param_2;
  *(undefined1 *)(param_1 + 0xb275) = param_3;
  *(undefined1 *)(param_1 + 0xb274) = param_4;
  *(undefined1 *)(param_1 + 0xb277) = 0xff;
  return;
}

