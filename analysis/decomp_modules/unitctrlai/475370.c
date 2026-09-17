
void FUN__text__00475370(int param_1,undefined1 param_2,char param_3)

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
  *(undefined1 *)(param_1 + 0x291) = 0;
  *local_c = param_2;
  *(undefined1 *)(param_1 + 0x292) = 0;
  *(undefined1 *)(param_1 + 0x293) = 0;
  if (param_3 != -1) {
    *(char *)(param_1 + 0x2a7) = param_3;
  }
  FUN__text__00475650(param_1);
  local_8 = 0x4753e0;
  FUN__text__0056ce80();
  return;
}

