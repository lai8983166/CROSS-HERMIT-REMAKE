
void __fastcall FUN__text__00457030(int param_1)

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
  FUN__text__00416fa0(param_1 + 0x117e58);
  *(undefined1 *)(local_8 + 0x113bfc) = *(undefined1 *)(local_8 + 0x2f0d4);
  *(undefined1 *)(local_8 + 0x113bfd) = 4;
  local_c = FUN__text__00419fe0(local_8 + 0x113bf0,*(undefined4 *)(local_8 + 0x113bf8));
  if (local_c != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cdc8 + 0x10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__00416ff0(local_8 + 0x117e58);
  FUN__text__00417050(local_8 + 0x117e58);
  local_8 = 0x457109;
  FUN__text__0056ce80();
  return;
}

