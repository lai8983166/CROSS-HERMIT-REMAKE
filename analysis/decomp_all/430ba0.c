
void FUN__text__00430ba0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00456b20();
  if ((iVar2 != 0) &&
     (iVar2 = FUN__text__00424f80("tTask->IsNetwork()==0",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff734 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x430c23;
  FUN__text__0056ce80();
  return;
}

