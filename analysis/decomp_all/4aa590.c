
void FUN__text__004aa590(short param_1)

{
  int iVar1;
  undefined2 uVar3;
  undefined4 uVar2;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  short local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1;
  uVar3 = (undefined2)((uint)(param_1 * 0x12) >> 0x10);
  uVar2 = CONCAT22(uVar3,*(undefined2 *)
                          (&DAT_0061b20a + *(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10));
  FUN__text__004d67f0(CONCAT31((int3)((uint)uVar2 >> 8),
                               (&DAT_0061b208)[*(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10]),
                      0x7e,uVar2,CONCAT22(uVar3,*(undefined2 *)(&DAT_0061b630 + param_1 * 0x12)),
                      CONCAT22((short)((uint)(param_1 * 0x12) >> 0x10),
                               *(undefined2 *)(&DAT_0061b632 + param_1 * 0x12)),
                      (uint)*(ushort *)
                             (&DAT_0061b20c + *(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10) +
                      (int)*(short *)(&DAT_0061b634 + param_1 * 0x12),
                      (uint)*(ushort *)
                             (&DAT_0061b20e + *(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10) +
                      (int)*(short *)(&DAT_0061b636 + param_1 * 0x12),
                      CONCAT22(0xcccc,*(undefined2 *)
                                       (&DAT_0061b210 +
                                       *(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10)),
                      CONCAT22(0xcccc,*(undefined2 *)
                                       (&DAT_0061b212 +
                                       *(short *)(&DAT_0061b62e + param_1 * 0x12) * 0x10)),8);
  local_8 = 0x4aa6ab;
  FUN__text__0056ce80();
  return;
}

