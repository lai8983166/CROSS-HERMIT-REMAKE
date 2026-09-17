
void __thiscall FUN__text__00425ed0(int param_1,int param_2)

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
  if (*(char *)(param_1 + 0x630) != '\0') {
    iVar2 = FUN__text__00424f80("ImeSysReqOpenStatus == 0",
                                "e:\\crosshermit\\game\\src\\system\\sysime.cpp",DAT_005ff67c + 1,0)
    ;
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (param_2 == 0) {
    *(undefined1 *)(local_8 + 0x630) = 0xff;
  }
  else {
    *(undefined1 *)(local_8 + 0x630) = 1;
  }
  local_8 = 0x425f4a;
  FUN__text__0056ce80();
  return;
}

