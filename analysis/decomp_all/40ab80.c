
void __thiscall FUN_0040ab80(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_2 + 8) == '\0') {
    local_c = *(int *)(param_2 + 0x20);
    while (local_c != 0) {
      local_10 = *(int *)(local_c + 0x20);
      if (*(char *)(local_c + 2) == '\0') {
        FUN_0040ab80(local_c);
      }
      local_c = local_10;
    }
    local_10 = 0;
  }
  else {
    if ((*(int *)(param_2 + 0x24) == 0) &&
       (iVar2 = FUN_00424f80("aw->top!=0","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                             DAT_005ff100 + 0x14,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    for (local_c = *(int *)(param_2 + 0x24); *(int *)(local_c + 0x20) != param_2;
        local_c = *(int *)(local_c + 0x20)) {
    }
    *(undefined4 *)(local_c + 0x20) = *(undefined4 *)(param_2 + 0x20);
    FUN_0040b660(param_2);
  }
  local_8 = 0x40ac7d;
  __chkesp();
  return;
}

