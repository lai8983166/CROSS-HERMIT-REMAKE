
void FUN__text__004591e0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [14];
  undefined4 uStack_30;
  int local_28;
  int local_24;
  int local_20;
  undefined4 local_1c;
  int local_18;
  undefined4 local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f7eb;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  local_24 = FUN__text__00428a40(0x14);
  local_8 = 0;
  if (local_24 == 0) {
    local_28 = 0;
  }
  else {
    local_28 = FUN__text__00459300(local_14);
  }
  local_20 = local_28;
  local_8 = 0xffffffff;
  local_18 = local_28;
  if (local_28 == 0) {
    iVar2 = FUN__text__00424f80("dlg!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cde8 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*DAT_0059238c)(PTR_IMAGE_DOS_HEADER_007a2728,0x87,PTR_DAT_007a0bb4,FUN__text__004593f0,0);
  FUN__text__0056ce80();
  (*DAT_00592354)(PTR_IMAGE_DOS_HEADER_007a2728,0x9a,PTR_DAT_007a0bb4,FUN__text__00424980,local_14);
  local_1c = FUN__text__0056ce80();
  ExceptionList = local_10;
  uStack_30 = 0x4592f2;
  FUN__text__0056ce80();
  return;
}

