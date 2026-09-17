
void FUN__text__004d4250(short param_1)

{
  short sVar1;
  int iVar2;
  uint uVar3;
  undefined2 uVar4;
  undefined4 *puVar5;
  undefined4 local_60 [16];
  undefined4 local_20;
  uint local_1c;
  short local_18;
  uint local_14;
  undefined4 local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar5 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if ((param_1 != 0) && (sVar1 = FUN__text__004d46e0(param_1), sVar1 != 0)) {
    if (param_1 < 0x65) {
      local_c = local_c & 0xffff0000;
      while (((int)(local_c & 0xffff) < (int)DAT_007a5260 &&
             (*(short *)(&DAT_007a5210 + (local_c & 0xffff) * 2) != param_1))) {
        local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
      }
      local_10 = CONCAT22(local_10._2_2_,(short)local_c);
      while ((int)(local_10 & 0xffff) < DAT_007a5260 + -1) {
        *(undefined2 *)(&DAT_007a5210 + (local_10 & 0xffff) * 2) =
             *(undefined2 *)(&DAT_007a5212 + (local_10 & 0xffff) * 2);
        local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
      }
      DAT_007a5260 = DAT_007a5260 + -1;
      local_10 = (uint)local_10._2_2_ << 0x10;
      while( true ) {
        uVar3 = local_10 & 0xffff;
        if (4 < uVar3) break;
        local_14 = local_14 & 0xffff0000;
        while ((local_14 & 0xffff) < 4) {
          if (*(short *)(&DAT_007aaa22 + (local_14 & 0xffff) * 2 + (local_10 & 0xffff) * 0x1c) ==
              param_1) {
            *(undefined2 *)(&DAT_007aaa22 + (local_14 & 0xffff) * 2 + (local_10 & 0xffff) * 0x1c) =
                 0xffff;
          }
          local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
        }
        local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
      }
      local_10 = (uint)local_10._2_2_ << 0x10;
      while (uVar4 = (undefined2)(uVar3 >> 0x10), (local_10 & 0xffff) < 8) {
        uVar3 = local_10 & 0xffff;
        local_18 = *(short *)(&DAT_007e184a + uVar3 * 2 + param_1 * 0x4a0);
        if ((0 < local_18) &&
           (uVar3 = (uint)local_18, (*(ushort *)(&DAT_007aacaa + uVar3 * 2) & 1) == 1)) {
          *(ushort *)(&DAT_007aacaa + local_18 * 2) =
               (ushort)CONCAT31((int3)(CONCAT22(local_18 >> 0xf,
                                                *(undefined2 *)(&DAT_007aacaa + local_18 * 2)) >> 8)
                                ,(char)*(undefined2 *)(&DAT_007aacaa + local_18 * 2)) | 1;
          uVar3 = CONCAT22(local_18 >> 0xf,*(undefined2 *)(&DAT_007aacaa + local_18 * 2)) &
                  0xfffff0ff | 0x100;
          *(short *)(&DAT_007aacaa + local_18 * 2) = (short)uVar3;
        }
        uVar3 = CONCAT22((short)(uVar3 >> 0x10),(short)local_10 + 1);
        local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
      }
    }
    else {
      local_1c = local_1c & 0xffff0000;
      while (((int)(local_1c & 0xffff) < (int)DAT_007a528a &&
             (*(short *)(&DAT_007a5262 + (local_1c & 0xffff) * 2) != param_1))) {
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_1c);
      while( true ) {
        iVar2 = DAT_007a528a + -1;
        if (iVar2 <= (int)(local_20 & 0xffff)) break;
        *(undefined2 *)(&DAT_007a5262 + (local_20 & 0xffff) * 2) =
             *(undefined2 *)(&DAT_007a5264 + (local_20 & 0xffff) * 2);
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      local_20 = (uint)local_20._2_2_ << 0x10;
      while (uVar4 = (undefined2)((uint)iVar2 >> 0x10), (local_20 & 0xffff) < 5) {
        iVar2 = (local_20 & 0xffff) * 0x1c;
        if (*(short *)(&DAT_007aaa12 + iVar2) == param_1) {
          iVar2 = (local_20 & 0xffff) * 0x1c;
          *(undefined2 *)(&DAT_007aaa12 + iVar2) = 0xffff;
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      DAT_007a528a = DAT_007a528a + -1;
    }
    FUN__text__004d4770(CONCAT22(uVar4,param_1));
  }
  local_8 = 0x4d45b0;
  FUN__text__0056ce80();
  return;
}

