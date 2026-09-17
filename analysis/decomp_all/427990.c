
void FUN__text__00427990(int *param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 *local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1 == (int *)0x0) {
    iVar2 = FUN__text__00424f80("tbl != 0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6b0 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (param_2 == (int *)0x0) {
    iVar2 = FUN__text__00424f80("lw != 0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6b0 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (param_1 == param_2) {
    iVar2 = FUN__text__00424f80("tbl != lw","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6b0 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (param_1[1] != 0) {
    local_c = (undefined4 *)param_1[1];
    *local_c = param_2;
  }
  *param_2 = (int)param_1;
  param_2[1] = param_1[1];
  param_1[1] = (int)param_2;
  local_8 = 0x427a71;
  FUN__text__0056ce80();
  return;
}

