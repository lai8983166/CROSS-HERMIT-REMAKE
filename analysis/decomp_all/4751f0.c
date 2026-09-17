
void FUN__text__004751f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined1 *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (undefined1 *)(param_1 + 0x290);
  if (*(char *)(param_1 + 0x292) != '\0') {
    *(undefined1 *)(param_1 + 0x291) = *local_c;
    *local_c = *(undefined1 *)(param_1 + 0x292);
    *(undefined1 *)(param_1 + 0x292) = 0;
    *(undefined1 *)(param_1 + 0x293) = 0;
    FUN__text__004756a0(param_1);
  }
  local_8 = 0x475269;
  FUN__text__0056ce80();
  return;
}

