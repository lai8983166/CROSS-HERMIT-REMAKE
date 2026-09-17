
void FUN__text__0049da20(int param_1,int param_2,short param_3,short param_4,undefined2 param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 == 0) &&
     (iVar2 = FUN__text__00424f80("wk!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                  DAT_0061b008 + 0x11,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_18 = param_2;
  if (param_2 == 0) {
    local_c = (uint)*(short *)(*(int *)(param_1 + 600) + 0x18);
  }
  else if (param_2 == 1) {
    local_c = (uint)*(short *)(*(int *)(param_1 + 600) + 0x1e);
  }
  else if (param_2 == 2) {
    local_c = (uint)*(ushort *)(*(int *)(param_1 + 600) + 0x2e);
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                DAT_0061b008 + 0x17,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = -1;
  local_14 = 0;
  do {
    if (local_14 == 8) {
LAB__text__0049db50:
      if ((local_10 == -1) &&
         (iVar2 = FUN__text__00424f80("level != -1",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                      DAT_0061b008 + 0x2c,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__004077c0(DAT_007a49fc);
      *(undefined2 *)(local_8 + 0xde808) = 0;
      FUN__text__00407870(0x5a,local_10 + 0xb);
      *(undefined4 *)(local_8 + 0xde80c) = 0;
      *(undefined2 *)(local_8 + 0xde826) = param_5;
      *(undefined1 *)(local_8 + 0xde817) = 0xff;
      *(undefined1 *)(local_8 + 0xde814) = 0x80;
      *(undefined1 *)(local_8 + 0xde815) = 0x80;
      *(undefined1 *)(local_8 + 0xde816) = 0x80;
      FUN__text__004079c0((int)param_3,(int)param_4);
      local_8 = 0x49dc1a;
      FUN__text__0056ce80();
      return;
    }
    if (param_2 == 2) {
      if ((int)local_c < (int)*(short *)(&UNK_006e4808 + (7 - local_14) * 2)) {
        local_10 = local_14;
        goto LAB__text__0049db50;
      }
    }
    else if ((int)local_c <= (int)*(short *)(&DAT_006e47e8 + local_14 * 2 + param_2 * 0x10)) {
      local_10 = local_14;
      goto LAB__text__0049db50;
    }
    local_14 = local_14 + 1;
  } while( true );
}

