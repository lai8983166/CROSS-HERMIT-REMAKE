
void FUN__text__004d0860(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined **ppuVar5;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  FUN__text__004cde10("data\\adv\\bin\\Gybc_00.bin",0x14);
  ppuVar5 = &PTR_s_data_Sound_plw_ARSND_SE_LUP00_wa_00624aa8;
  uVar2 = FUN__text__00450110(&DAT_005953ac);
  local_c = FUN__text__0040c780(2,uVar2,ppuVar5);
  if (local_c != 0) {
    iVar3 = FUN__text__00424f80("ret == 0","E:\\CrossHermit\\GAME\\SRC\\YOSHIMARU\\YBC\\YBC32.CPP",
                                DAT_00624ac8 + 0x11,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4d08f1;
  FUN__text__0056ce80();
  return;
}

