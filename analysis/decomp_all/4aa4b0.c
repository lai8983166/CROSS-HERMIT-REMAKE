
void FUN__text__004aa4b0(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  uint local_20;
  short local_1c;
  undefined4 local_18;
  uint local_14;
  undefined4 local_8;
  
  puVar4 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_1c = -1;
  local_20 = local_20 & 0xffff0000;
  do {
    iVar2 = (local_20 & 0xffff) * 0x12;
    if (*(short *)(&DAT_0061b628 + iVar2) < 0) {
LAB__text__004aa570:
      local_8 = 0x4aa581;
      FUN__text__0056ce80();
      return;
    }
    local_18 = 0;
    local_14 = 0;
    iVar1 = (local_20 & 0xffff) * 0x12;
    iVar3 = (local_20 & 0xffff) * 0x12;
    FUN__text__004d5ca0(&local_18,
                        CONCAT22((short)((uint)iVar3 >> 0x10),
                                 *(undefined2 *)(&DAT_0061b628 + (local_20 & 0xffff) * 0x12)),
                        CONCAT22((short)((uint)iVar1 >> 0x10),*(undefined2 *)(&DAT_0061b62a + iVar3)
                                ),
                        CONCAT22((short)((uint)iVar2 >> 0x10),*(undefined2 *)(&DAT_0061b62c + iVar1)
                                ));
    if ((local_14 & 1) != 0) {
      local_1c = (short)local_20;
      goto LAB__text__004aa570;
    }
    local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
  } while( true );
}

