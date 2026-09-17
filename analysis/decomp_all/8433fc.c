
void FUN__text1__008433fc(int param_1,int param_2,int param_3)

{
  ushort uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_1c = 0xffffffff;
  local_8 = 0;
  local_10 = 7;
  local_14 = 4;
  if (*(ushort *)(param_2 + 2) == 0) {
    local_10 = 0x8a;
    local_14 = 3;
  }
  local_c = (uint)*(ushort *)(param_2 + 2);
  for (local_20 = 0; local_20 <= param_3; local_20 = local_20 + 1) {
    uVar3 = (uint)*(ushort *)(param_2 + 6 + local_20 * 4);
    iVar4 = local_8 + 1;
    if ((local_10 <= iVar4) || (local_c != uVar3)) {
      if (iVar4 < local_14) {
        do {
          local_8 = iVar4;
          uVar2 = (uint)*(ushort *)(param_1 + 0xa76 + local_c * 4);
          if ((int)(0x10 - uVar2) < *(int *)(param_1 + 0x16b4)) {
            uVar1 = *(ushort *)(param_1 + 0xa74 + local_c * 4);
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uint)uVar1 >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar2;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 *(short *)(param_1 + 0xa74 + local_c * 4) <<
                 ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar2;
          }
          iVar4 = local_8 + -1;
        } while (local_8 + -1 != 0);
      }
      else if (local_c == 0) {
        if (iVar4 < 0xb) {
          uVar2 = (uint)*(ushort *)(param_1 + 0xaba);
          if ((int)(0x10 - uVar2) < *(int *)(param_1 + 0x16b4)) {
            uVar1 = *(ushort *)(param_1 + 0xab8);
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uint)uVar1 >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar2;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 *(short *)(param_1 + 0xab8) << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar2;
          }
          if (*(int *)(param_1 + 0x16b4) < 0xe) {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(local_8 + -2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 3;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(local_8 - 2U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(local_8 - 2U & 0xffff) >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xd;
          }
        }
        else {
          uVar2 = (uint)*(ushort *)(param_1 + 0xabe);
          if ((int)(0x10 - uVar2) < *(int *)(param_1 + 0x16b4)) {
            uVar1 = *(ushort *)(param_1 + 0xabc);
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uint)uVar1 >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar2;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 *(short *)(param_1 + 0xabc) << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar2;
          }
          if (*(int *)(param_1 + 0x16b4) < 10) {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(local_8 + -10 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 7;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(local_8 - 10U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(local_8 - 10U & 0xffff) >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -9;
          }
        }
      }
      else {
        if (local_c != local_1c) {
          uVar2 = (uint)*(ushort *)(param_1 + 0xa76 + local_c * 4);
          iVar4 = local_8;
          if ((int)(0x10 - uVar2) < *(int *)(param_1 + 0x16b4)) {
            uVar1 = *(ushort *)(param_1 + 0xa74 + local_c * 4);
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uint)uVar1 >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar2;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 *(short *)(param_1 + 0xa74 + local_c * 4) <<
                 ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
            *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar2;
          }
        }
        local_8 = iVar4;
        uVar2 = (uint)*(ushort *)(param_1 + 0xab6);
        if ((int)(0x10 - uVar2) < *(int *)(param_1 + 0x16b4)) {
          uVar1 = *(ushort *)(param_1 + 0xab4);
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               uVar1 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)*(undefined2 *)(param_1 + 0x16b0);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(short *)(param_1 + 0x16b0) =
               (short)((int)(uint)uVar1 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f))
          ;
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar2;
        }
        else {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               *(short *)(param_1 + 0xab4) << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar2;
        }
        if (*(int *)(param_1 + 0x16b4) < 0xf) {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               (ushort)(local_8 + -3 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
          *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + 2;
        }
        else {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               (ushort)(local_8 - 3U << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)*(undefined2 *)(param_1 + 0x16b0);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(short *)(param_1 + 0x16b0) =
               (short)((int)(local_8 - 3U & 0xffff) >>
                      (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
          *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0xe;
        }
      }
      local_8 = 0;
      local_1c = local_c;
      iVar4 = local_8;
      if (uVar3 == 0) {
        local_10 = 0x8a;
        local_14 = 3;
      }
      else if (local_c == uVar3) {
        local_10 = 6;
        local_14 = 3;
      }
      else {
        local_10 = 7;
        local_14 = 4;
      }
    }
    local_8 = iVar4;
    local_c = uVar3;
  }
  return;
}

