
void __fastcall FUN__text__00427f70(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_1[1] == 0) {
    iVar2 = FUN__text__00424f80("ListWork!=0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6c4 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*local_8 == 0) {
    iVar2 = FUN__text__00424f80("ListCnt!=0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6c4 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8[3] = 0;
  local_8[4] = 0;
  local_8[5] = 0;
  local_8[6] = 0;
  local_8[7] = 0;
  local_8[8] = 0;
  for (local_c = 0; local_c != *local_8; local_c = local_c + 1) {
    FUN__text__00427cd0(local_8[1] + local_c * 0xc);
  }
  local_8 = (int *)0x428064;
  FUN__text__0056ce80();
  return;
}

