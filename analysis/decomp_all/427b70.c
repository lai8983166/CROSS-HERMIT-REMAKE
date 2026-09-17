
void __thiscall FUN__text__00427b70(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 != param_1 + 0xc) && (param_2 != param_1 + 0x18)) {
    iVar2 = FUN__text__00424f80("(top==&Open) || (top==&Close)",
                                "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                DAT_005ff6b8 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined4 *)(local_8 + 0x24) = *(undefined4 *)(param_2 + 4);
  local_8 = 0x427be0;
  FUN__text__0056ce80();
  return;
}

