
void __thiscall FUN__text__00427ae0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_2 != param_1 + 0xc) && (param_2 != param_1 + 0x18)) &&
     (iVar2 = FUN__text__00424f80("(top==&Open) || (top==&Close)",
                                  "e:\\crosshermit\\game\\src\\system\\syslinklist.cpp",
                                  DAT_005ff6b4 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(param_2 + 4) != 0) {
    local_c = *(undefined4 *)(param_2 + 4);
    FUN__text__00427a80(local_c);
  }
  local_8 = 0x427b69;
  FUN__text__0056ce80();
  return;
}

