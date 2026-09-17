
void FUN__text__004d3e90(short param_1,short param_2,short param_3)

{
  ushort uVar1;
  short sVar2;
  ushort uVar3;
  int iVar4;
  uint uVar5;
  undefined2 extraout_var;
  undefined4 *puVar6;
  undefined4 local_15c [16];
  int local_11c;
  ushort local_118;
  undefined2 uStack_116;
  undefined1 local_114 [16];
  undefined1 local_104;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  ushort local_c;
  undefined2 uStack_a;
  undefined4 local_8;
  
  puVar6 = local_15c;
  for (iVar4 = 0x56; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  if ((param_1 != 0) &&
     (sVar2 = FUN__text__004d46e0(param_1), uVar1 = DAT_007a528a, uVar3 = DAT_007a5260, sVar2 == 0))
  {
    if (param_1 < 0x65) {
      _local_c = CONCAT22(uStack_a,DAT_007a5260);
      uVar5 = (uint)DAT_007a5260;
      DAT_007a5260 = DAT_007a5260 + 1;
      *(short *)(&DAT_007a5210 + uVar5 * 2) = param_1;
      if ((-1 < param_2) && (-1 < param_3)) {
        *(ushort *)(&DAT_007aaae0 + param_2 * 8 + param_3 * 2) = uVar3;
        *(short *)(&DAT_007aaab8 + param_2 * 8 + param_3 * 2) = param_1;
        *(short *)(&DAT_007aaa22 + param_3 * 2 + param_2 * 0x1c) = param_1;
      }
      for (local_10 = 0; local_10 < 0x20; local_10 = local_10 + 1) {
        (&DAT_007cf445)[(int)local_10 + param_1 * 0x124] = 0;
      }
      (&DAT_007cf444)[(int)*(short *)(&DAT_007e17ee + param_1 * 0x4a0) + param_1 * 0x124] = 1;
      iVar4 = 0;
      for (local_18 = 0; local_18 < 8; local_18 = local_18 + 1) {
        local_14 = *(short *)(&DAT_007e184a + local_18 * 2 + param_1 * 0x4a0);
        iVar4 = (int)local_14;
        if (0 < iVar4) {
          if ((*(ushort *)(&DAT_007aacaa + local_14 * 2) & 1) == 1) {
            iVar4 = param_1 * 0x4a0;
            *(undefined2 *)(&DAT_007e184a + local_18 * 2 + iVar4) = 0;
          }
          else {
            *(ushort *)(&DAT_007aacaa + local_14 * 2) =
                 (ushort)CONCAT31((int3)(CONCAT22(local_14 >> 0xf,
                                                  *(undefined2 *)(&DAT_007aacaa + local_14 * 2)) >>
                                        8),(char)*(undefined2 *)(&DAT_007aacaa + local_14 * 2)) | 1;
            uVar5 = CONCAT22(local_14 >> 0xf,*(undefined2 *)(&DAT_007aacaa + local_14 * 2)) &
                    0xfffff0ff;
            *(ushort *)(&DAT_007aacaa + local_14 * 2) = (ushort)uVar5 | 0x300;
            uVar5 = CONCAT22((short)(uVar5 >> 0x10),param_1) & 0xffff007f;
            uVar3 = (short)uVar5 << 1;
            iVar4 = CONCAT22((short)(uVar5 >> 0x10),uVar3);
            *(ushort *)(&DAT_007aacaa + local_14 * 2) =
                 *(ushort *)(&DAT_007aacaa + local_14 * 2) & 0xff01 | uVar3;
          }
        }
      }
      local_18 = 0;
      while (local_18 < 8) {
        local_1c = *(short *)(&DAT_007e183a + local_18 * 2 + param_1 * 0x4a0);
        iVar4 = (int)local_18;
        if (0 < local_1c) {
          local_11c = (int)DAT_007a528c;
          if ((local_11c < 0) || (1 < local_11c)) {
            *(undefined2 *)(&DAT_007e183a + local_18 * 2 + param_1 * 0x4a0) = 0;
            iVar4 = param_1 * 0x4a0;
          }
          else {
            (&DAT_007e18a0)[(local_1c + -1) * 0xc + param_1 * 0x4a0] = 6;
            iVar4 = local_11c;
          }
        }
        local_18 = local_18 + 1;
        iVar4 = CONCAT22((short)((uint)iVar4 >> 0x10),local_18);
      }
      FUN__text__004d58e0(local_114,CONCAT22((short)((uint)iVar4 >> 0x10),param_1));
      (&DAT_007e1838)[param_1 * 0x4a0] = local_104;
      FUN__text__004d3aa0(CONCAT22(extraout_var,param_1));
    }
    else {
      _local_118 = CONCAT22(uStack_116,DAT_007a528a);
      uVar5 = (uint)DAT_007a528a;
      DAT_007a528a = DAT_007a528a + 1;
      *(short *)(&DAT_007a5262 + uVar5 * 2) = param_1;
      if (-1 < param_2) {
        *(ushort *)(&DAT_007aaaae + param_2 * 2) = uVar1;
        *(short *)(&DAT_007aaaa4 + param_2 * 2) = param_1;
        *(short *)(&DAT_007aaa12 + param_2 * 0x1c) = param_1;
      }
    }
    FUN__text__004d4730(param_1);
  }
  local_8 = 0x4d4243;
  FUN__text__0056ce80();
  return;
}

