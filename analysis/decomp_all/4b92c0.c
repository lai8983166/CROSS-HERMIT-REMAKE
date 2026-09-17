
void FUN__text__004b92c0(void)

{
  undefined2 uVar1;
  undefined2 extraout_var;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  uint local_8;
  
  uVar1 = 0xcccc;
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = local_8 & 0xffff0000;
  while ((short)local_8 < DAT_007a4ae8) {
    FUN__text__004b9340(CONCAT22(DAT_007a4ae8 >> 0xf,
                                 *(undefined2 *)(&DAT_007a4aec + (short)local_8 * 2)),
                        CONCAT22(uVar1,(short)local_8));
    uVar1 = extraout_var;
    local_8 = CONCAT22(local_8._2_2_,(short)local_8 + 1);
  }
  DAT_007f448c._1_1_ = (undefined1)DAT_007a4ae8;
  local_8 = 0x4b932e;
  FUN__text__0056ce80();
  return;
}

