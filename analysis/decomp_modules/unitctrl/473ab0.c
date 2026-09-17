
void FUN__text__00473ab0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
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
  iVar2 = FUN__text__00456b20();
  if (iVar2 == 0) {
    for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
      *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0) = 0;
      *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0) = 0;
      (&DAT_007f45c6)[local_c * 0xb0] = 0;
    }
    local_10 = 0;
    for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
      local_14 = local_8 + 0x80aec + local_c * 0x520;
      iVar2 = FUN__text__00468d10(local_14);
      if ((iVar2 != 0) && (iVar2 = FUN__text__0046a4c0(local_14), iVar2 != 0)) {
        if ((*(short *)(&DAT_007f451a + local_c * 0xb0) != *(short *)(*(int *)(local_14 + 600) + 2))
           && (iVar2 = FUN__text__00424f80("GameWorkUnit[i].char_no == wk->data->char_no",
                                           "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                           DAT_00618c40 + 0x35,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        if ((*(short *)(&DAT_007f4518 + local_c * 0xb0) != **(short **)(local_14 + 600)) &&
           (iVar2 = FUN__text__00424f80("GameWorkUnit[i].no == wk->data->no",
                                        "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                        DAT_00618c40 + 0x36,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0) =
             *(undefined2 *)(*(int *)(local_14 + 600) + 0xaa);
        *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0) =
             *(undefined2 *)(*(int *)(local_14 + 600) + 0xac);
        (&DAT_007f45c6)[local_c * 0xb0] = *(undefined1 *)(*(int *)(local_14 + 600) + 0xae);
      }
    }
    DAT_007f4512 = *(undefined2 *)(local_8 + 0x2ef14);
  }
  else {
    iVar2 = FUN__text__004daae0((int)DAT_007f4488);
    if (iVar2 != 0) {
      for (local_c = 0; local_c != 0x50; local_c = local_c + 1) {
        *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0) = 0;
        *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0) = 0;
        (&DAT_007f45c6)[local_c * 0xb0] = 0;
      }
      _memset(&DAT_007f4518,0,0x3700);
      local_10 = 0;
      for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
        local_14 = local_8 + 0x80aec + local_c * 0x520;
        puVar3 = *(undefined4 **)(local_8 + 0x80d44 + local_c * 0x520);
        puVar4 = (undefined4 *)(&DAT_007f4518 + local_10 * 0xb0);
        for (iVar2 = 0x2c; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar4 = puVar4 + 1;
        }
        local_10 = local_10 + 1;
      }
      DAT_007f4512 = *(undefined2 *)(local_8 + 0x2ef14 + (uint)*(byte *)(local_8 + 0x2ef44) * 2);
    }
  }
  local_8 = 0x473db0;
  FUN__text__0056ce80();
  return;
}

