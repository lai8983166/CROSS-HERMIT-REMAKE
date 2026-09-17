
void FUN__text__004ab0d0(byte param_1,char param_2,char param_3,undefined2 param_4)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  ushort local_c;
  undefined2 uStack_a;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = (ushort)param_1;
  _local_c = CONCAT22(uStack_a,uVar1);
  if ((&DAT_0061b639)[(uint)uVar1 * 0x12] != '\0') {
    FUN__text__004d2790(&DAT_0061b208 + *(short *)(&DAT_0061b62e + (uint)uVar1 * 0x12) * 0x10,
                        CONCAT11((char)((ushort)*(undefined2 *)(&DAT_0061b630 + (uint)uVar1 * 0x12)
                                       >> 8),(&DAT_0061b638)[(uint)uVar1 * 0x12]),param_4,
                        *(undefined2 *)(&DAT_0061b630 + (uint)uVar1 * 0x12),
                        CONCAT22(0xcccc,*(undefined2 *)(&DAT_0061b632 + (uint)uVar1 * 0x12)),
                        (short)param_2,CONCAT22(0xcccc,(short)param_3));
  }
  local_8 = 0x4ab190;
  FUN__text__0056ce80();
  return;
}

