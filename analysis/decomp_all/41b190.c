
undefined4 __fastcall FUN__text__0041b190(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    if (*(char *)(param_1 + 0x1780 + local_c * 0x88) != '\0') {
      *(undefined1 *)(param_1 + 0x1781 + local_c * 0x88) = 0;
    }
  }
  return 0;
}

