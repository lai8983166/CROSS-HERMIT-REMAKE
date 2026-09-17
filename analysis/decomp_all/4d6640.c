
void __fastcall FUN_004d6640(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x6418) != '\0') {
    local_c = *(undefined4 *)(param_1 + 0x6414);
    FUN_00428ad0(local_c);
  }
  *(undefined1 *)(local_8 + 0x6418) = 0;
  local_8 = 0x4d669b;
  __chkesp();
  return;
}

