
undefined1 __fastcall FUN__text__004c70e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 2) == '\0') {
    *(undefined1 *)(param_1 + 2) = 1;
  }
  else {
    *(undefined1 *)(param_1 + 2) = 0;
  }
  return *(undefined1 *)(param_1 + 2);
}

