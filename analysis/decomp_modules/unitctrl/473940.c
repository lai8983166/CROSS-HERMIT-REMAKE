
void __fastcall FUN__text__00473940(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  local_8 = param_1;
  do {
    if (local_c == 0x10) {
      local_8 = 0x473aa5;
      FUN__text__0056ce80();
      return;
    }
    local_10 = (int)(char)(&DAT_007f44be)[local_c];
    if (local_10 != 0) {
      if (((local_10 < 0) || (0xf9 < local_10)) &&
         (iVar2 = FUN__text__00424f80("(0<=unit_no) && (unit_no<(250))",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618c3c + 8,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_14 = local_8 + 0x80aec + (0xf9 - (local_10 + -1)) * 0x520;
      if (((*(short *)(*(int *)(local_14 + 600) + 2) != 0x195) &&
          (*(short *)(*(int *)(local_14 + 600) + 2) != 0x196)) &&
         (iVar2 = FUN__text__00424f80("(wk->data->char_no==405) || (wk->data->char_no==406)",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618c3c + 0xb,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      iVar2 = FUN__text__00456b20();
      if (iVar2 == 0) {
        iVar2 = FUN__text__0046a430(local_14);
        if (iVar2 == 0) {
          (&DAT_007f44be)[local_c] = 0;
        }
        else {
          (&DAT_007f44be)[local_c] = 1;
        }
      }
      else {
        iVar2 = FUN__text__00468d80(local_14);
        if (iVar2 == 0) {
          (&DAT_007f44be)[local_c] = 0;
        }
        else {
          (&DAT_007f44be)[local_c] = 1;
        }
      }
    }
    local_c = local_c + 1;
  } while( true );
}

