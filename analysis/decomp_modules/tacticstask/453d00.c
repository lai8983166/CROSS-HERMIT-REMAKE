
void FUN__text__00453d00(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  char local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  iVar2 = FUN__text__00456b20();
  if ((iVar2 != 0) &&
     (iVar2 = FUN__text__00424f80("IsNetwork()==0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cd80 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_18 = *(char *)(local_8 + 0x30);
  if (local_18 == '\x01') {
    local_c = 0x179;
    local_10 = 0x144;
    local_1c = FUN__text__004586d0(0x179,0x144);
    if (local_1c == 0) {
      local_14 = 0;
    }
    else if (local_1c == 1) {
      local_14 = 0;
      *(undefined1 *)(local_8 + 0x30) = 0;
    }
    else if (local_1c == 2) {
      DAT_005ff720 = 0xffffffff;
      *(undefined1 *)(local_8 + 0x31) = 1;
      local_14 = 1;
    }
  }
  else if ((local_18 == '\x02') && (iVar2 = FUN__text__00458d70(), iVar2 != 0)) {
    local_14 = 0;
    *(undefined1 *)(local_8 + 0x30) = 0;
  }
  local_8 = 0x453e00;
  FUN__text__0056ce80();
  return;
}

