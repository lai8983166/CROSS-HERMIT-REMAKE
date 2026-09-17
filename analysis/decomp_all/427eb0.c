
void __fastcall FUN__text__00427eb0(int *param_1)

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
                                DAT_005ff6c0 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*local_8 == 0) {
    iVar2 = FUN__text__00424f80("ListCnt!=0","e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6c0 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  while (local_c = FUN__text__00427ae0(local_8 + 3), local_c != 0) {
    FUN__text__00427cd0(local_c);
  }
  local_8 = (int *)0x427f64;
  FUN__text__0056ce80();
  return;
}

