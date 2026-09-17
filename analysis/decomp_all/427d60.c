
void __fastcall FUN__text__00427d60(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x1c) == 0) &&
     (iVar2 = FUN__text__00424f80("Close.next!=0",
                                  "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                  DAT_005ff6bc + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x1c) != 0) {
    local_c = *(int *)(local_8 + 0x1c);
    *(undefined4 *)(local_8 + 0x1c) = *(undefined4 *)(local_c + 4);
  }
  local_8 = 0x427ddc;
  FUN__text__0056ce80();
  return;
}

