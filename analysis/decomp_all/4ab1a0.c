
void FUN__text__004ab1a0(byte param_1,char param_2,char param_3,char param_4,char param_5,
                        undefined2 param_6)

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
                        CONCAT31((int3)(CONCAT22(0xcccc,(short)param_2) >> 8),
                                 (&DAT_0061b638)[(uint)uVar1 * 0x12]),param_6,
                        CONCAT22(0xcccc,(short)param_2),
                        CONCAT22((char)(&DAT_0061b639)[(uint)uVar1 * 0x12] >> 7,(short)param_3),
                        (short)param_4,CONCAT22(0xcccc,(short)param_5));
  }
  local_8 = 0x4ab246;
  FUN__text__0056ce80();
  return;
}

