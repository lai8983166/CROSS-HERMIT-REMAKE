
void __thiscall FUN__text__004801e0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_2 < 0) || (0xf9 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=unit_workno)&&(unit_workno<(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e98 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = local_8 + 0x80aec + param_2 * 0x520;
  iVar2 = FUN__text__00468d80(local_14);
  local_10 = (uint)(iVar2 != 0);
  iVar2 = FUN__text__00468d10(local_14);
  if (iVar2 == 0) {
    iVar2 = FUN__text__00424f80(&DAT_0059d748,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e98 + 0xc,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    iVar2 = FUN__text__004695d0(local_14);
    if (iVar2 == 0) {
      local_c = 0;
      iVar2 = FUN__text__00468d10(local_14);
      if (((iVar2 != 0) && (iVar2 = FUN__text__00469480(local_14), iVar2 != 0)) &&
         (iVar2 = FUN__text__00480320(local_10,local_14), iVar2 != 0)) {
        local_c = local_c + 1;
      }
    }
  }
  local_8 = 0x48030f;
  FUN__text__0056ce80();
  return;
}

