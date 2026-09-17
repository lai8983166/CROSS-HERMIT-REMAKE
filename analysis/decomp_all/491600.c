
void __thiscall FUN__text__00491600(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(short *)(param_1 + 0x30992) == -1) ||
     (*(short *)(param_2 + 2) !=
      *(short *)(param_1 + *(short *)(param_1 + 0x30992) * 0x520 + 0x80aee))) {
    *(undefined1 *)(param_1 + 0x30994) = 10;
  }
  else {
    *(undefined1 *)(param_1 + 0x30994) = 9;
  }
  return;
}

