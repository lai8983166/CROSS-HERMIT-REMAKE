
undefined2 __fastcall FUN__text__004cb180(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined2 local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x14) == '\0') {
    local_c = *(undefined2 *)(param_1 + 0xc);
  }
  else {
    local_c = *(undefined2 *)(param_1 + 0xe);
  }
  return local_c;
}

