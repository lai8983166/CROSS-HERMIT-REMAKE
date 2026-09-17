
uint FUN__text__004a2980(short param_1)

{
  short sVar1;
  short sVar2;
  uint uVar3;
  short sVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_5c [20];
  short local_c;
  
  uVar3 = 0xcccccccc;
  puVar6 = local_5c;
  for (iVar5 = 0x16; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_c = 0;
  while (local_c < 3) {
    (&DAT_007d6a14)[local_c] = 0;
    *(undefined2 *)(&DAT_007d6a1a + local_c * 2) = 0;
    *(undefined2 *)(&DAT_007d6a20 + local_c * 2) = 0;
    sVar4 = local_c >> 0xf;
    local_c = local_c + 1;
    uVar3 = CONCAT22(sVar4,local_c);
  }
  if (param_1 < 0) {
    uVar3 = uVar3 & 0xffffff00;
  }
  else {
    local_c = 0;
    while (local_c < 100) {
      iVar5 = local_c * 10;
      if (((&DAT_007a5bca)[iVar5 + param_1 * 1000] != '\0') &&
         (iVar5 = local_c * 10, (&DAT_007a5bcb)[iVar5 + param_1 * 1000] == '\0')) {
        sVar4 = *(short *)(&DAT_007a5bcc + local_c * 10 + param_1 * 1000);
        sVar2 = *(short *)(&DAT_0074bed6 + sVar4 * 0x60) + -1;
        sVar1 = (&DAT_007d6a14)[sVar2];
        (&DAT_007d6a14)[sVar2] = (&DAT_007d6a14)[sVar2] + 1;
        *(short *)(&DAT_007d630c + sVar1 * 6 + sVar2 * 600) =
             *(short *)(&DAT_0074bed8 + sVar4 * 0x60) + -1;
        *(short *)(&DAT_007d630e + sVar1 * 6 + sVar2 * 600) = sVar4;
        iVar5 = CONCAT22((short)((uint)(sVar1 * 6) >> 0x10),sVar1);
        *(short *)(&DAT_007d6310 + sVar1 * 6 + sVar2 * 600) = sVar1;
      }
      local_c = local_c + 1;
      uVar3 = CONCAT22((short)((uint)iVar5 >> 0x10),local_c);
    }
    local_c = 0;
    while (local_c < 3) {
      iVar5 = 0;
      if (10 < (ushort)(&DAT_007d6a14)[local_c]) {
        iVar5 = (int)((ushort)(&DAT_007d6a14)[local_c] - 9) / 2;
        *(short *)(&DAT_007d6a20 + local_c * 2) = (short)iVar5;
      }
      local_c = local_c + 1;
      uVar3 = CONCAT22((short)((uint)iVar5 >> 0x10),local_c);
    }
    uVar3 = CONCAT31((int3)(uVar3 >> 8),1);
  }
  return uVar3;
}

