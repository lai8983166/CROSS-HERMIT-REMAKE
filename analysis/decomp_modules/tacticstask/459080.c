
void __fastcall FUN__text__00459080(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = 0;
  local_8 = param_1;
  do {
    if (local_c == 0xc) {
LAB__text__004591c6:
      local_8 = 0x4591d3;
      FUN__text__0056ce80();
      return;
    }
    for (local_10 = 0; local_10 != 0x14; local_10 = local_10 + 1) {
      *(undefined **)(local_8 + 0x1194a0 + local_10 * 4) = &DAT_007a4398;
    }
    for (local_10 = 0; local_10 != 9; local_10 = local_10 + 1) {
      FUN__text__0056d810(local_8 + 0x11804d + local_10 * 0x104,
                          "data\\Sound\\plw\\UnitVoice\\tv%03d%s",local_c + 1,
                          (&PTR_s__0007_wav_0060cd04)[local_10]);
      *(int *)(local_8 + 0x1194a0 + local_10 * 4) = local_8 + 0x11804d + local_10 * 0x104;
    }
    iVar3 = local_8 + 0x1194a0;
    uVar2 = FUN__text__00450110(&DAT_005953ac);
    local_14 = FUN__text__0040c780(local_c + 7,uVar2,iVar3);
    if (local_14 != 0) {
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cde4 + 0x27,0);
      if (iVar3 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__004591c6;
    }
    local_c = local_c + 1;
  } while( true );
}

