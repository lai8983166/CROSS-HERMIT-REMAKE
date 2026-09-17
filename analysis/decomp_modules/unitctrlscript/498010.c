
void FUN__text__00498010(int param_1,int param_2)

{
  short sVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((*(char *)(DAT_007a49f8 + 0x2499) != '\0') &&
     (iVar3 = FUN__text__00424f80(&DAT_0059e908,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                  DAT_00619fd4 + 4,0), iVar3 != 0)) {
    pcVar2 = (code *)swi(3);
    (*pcVar2)();
    return;
  }
  *(undefined1 *)(DAT_007a49f8 + 0x24a8) = 0;
  sVar1 = *(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 4);
  local_8 = CONCAT22(local_8._2_2_,sVar1);
  local_c = *(short *)(*(int *)(DAT_007a49f4 + 0x2a494) + 6);
  if (((param_1 < 0) || (sVar1 <= param_1)) &&
     (iVar3 = FUN__text__00424f80("(0<=cx)&&(cx<mw)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                  DAT_00619fd4 + 0xb,0), iVar3 != 0)) {
    pcVar2 = (code *)swi(3);
    (*pcVar2)();
    return;
  }
  if (((param_2 < 0) || (local_c <= param_2)) &&
     (iVar3 = FUN__text__00424f80("(0<=cy)&&(cy<mh)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                  DAT_00619fd4 + 0xc,0), iVar3 != 0)) {
    pcVar2 = (code *)swi(3);
    (*pcVar2)();
    return;
  }
  param_1 = param_1 * 0x20 + -0x1f0;
  param_2 = param_2 * 0x10 + -0x115;
  if (param_1 < 0) {
    param_1 = 0;
  }
  if ((short)local_8 * 0x20 + -0x400 <= param_1) {
    param_1 = (short)local_8 * 0x20 + -0x400;
  }
  if (param_2 < 0) {
    param_2 = 0;
  }
  if (local_c * 0x10 + -0x238 <= param_2) {
    param_2 = local_c * 0x10 + -0x238;
  }
  local_10 = (short)((int)((int)*(short *)(DAT_007a49f4 + 0x2a49e) +
                          ((int)*(short *)(DAT_007a49f4 + 0x2a49e) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (short)((int)((int)*(short *)(DAT_007a49f4 + 0x2a4a0) +
                          ((int)*(short *)(DAT_007a49f4 + 0x2a4a0) >> 0x1f & 0xfU)) >> 4);
  if (((int)local_10 == (int)(param_1 + (param_1 >> 0x1f & 0x1fU)) >> 5) &&
     ((int)local_14 == (int)(param_2 + (param_2 >> 0x1f & 0xfU)) >> 4)) {
    *(undefined1 *)(DAT_007a49f8 + 0x24a8) = 0;
    FUN__text__004977a0();
  }
  else {
    *(undefined2 *)(DAT_007a49f8 + 0x24aa) = (undefined2)param_1;
    *(undefined2 *)(DAT_007a49f8 + 0x24ac) = (undefined2)param_2;
    *(int *)(DAT_007a49f8 + 0x24b0) = (int)*(short *)(DAT_007a49f4 + 0x2a49e) << 0x10;
    *(int *)(DAT_007a49f8 + 0x24b4) = (int)*(short *)(DAT_007a49f4 + 0x2a4a0) << 0x10;
    *(undefined1 *)(DAT_007a49f8 + 0x24a8) = 1;
    FUN__text__004977d0();
  }
  local_8 = 0x498271;
  FUN__text__0056ce80();
  return;
}

