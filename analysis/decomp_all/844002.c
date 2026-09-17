
void FUN__text1__00844002(int param_1,int param_2,int param_3)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint local_4c;
  uint local_18;
  
  local_18 = 0;
  if (*(int *)(param_1 + 0x1698) != 0) {
    do {
      uVar4 = (uint)*(ushort *)(*(int *)(param_1 + 0x169c) + local_18 * 2);
      uVar5 = (uint)*(byte *)(*(int *)(param_1 + 0x1690) + local_18);
      local_18 = local_18 + 1;
      if (uVar4 == 0) {
        uVar4 = (uint)*(ushort *)(param_2 + 2 + uVar5 * 4);
        if ((int)(0x10 - uVar4) < *(int *)(param_1 + 0x16b4)) {
          uVar2 = *(ushort *)(param_2 + uVar5 * 4);
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               uVar2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)*(undefined2 *)(param_1 + 0x16b0);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(short *)(param_1 + 0x16b0) =
               (short)((int)(uint)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f))
          ;
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar4;
        }
        else {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               *(short *)(param_2 + uVar5 * 4) << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar4;
        }
      }
      else {
        uVar6 = (uint)(byte)(&DAT_00873b38)[uVar5];
        uVar7 = (uint)*(ushort *)(param_2 + 0x406 + uVar6 * 4);
        if ((int)(0x10 - uVar7) < *(int *)(param_1 + 0x16b4)) {
          uVar2 = *(ushort *)(param_2 + 0x404 + uVar6 * 4);
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               uVar2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)*(undefined2 *)(param_1 + 0x16b0);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(short *)(param_1 + 0x16b0) =
               (short)((int)(uint)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f))
          ;
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar7;
        }
        else {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               *(short *)(param_2 + 0x404 + uVar6 * 4) <<
               ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar7;
        }
        iVar3 = *(int *)(&DAT_008732f4 + uVar6 * 4);
        if (iVar3 != 0) {
          uVar5 = uVar5 - *(int *)(&DAT_00873c38 + uVar6 * 4);
          if (0x10 - iVar3 < *(int *)(param_1 + 0x16b4)) {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(uVar5 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uVar5 & 0xffff) >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + iVar3;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(uVar5 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + iVar3;
          }
        }
        uVar5 = uVar4 - 1;
        if (uVar5 < 0x100) {
          bVar1 = (&DAT_00873937)[uVar4];
        }
        else {
          bVar1 = (&DAT_00873a38)[uVar5 >> 7];
        }
        local_4c = (uint)bVar1;
        uVar4 = (uint)*(ushort *)(param_3 + 2 + local_4c * 4);
        if ((int)(0x10 - uVar4) < *(int *)(param_1 + 0x16b4)) {
          uVar2 = *(ushort *)(param_3 + local_4c * 4);
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               uVar2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)*(undefined2 *)(param_1 + 0x16b0);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
               (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          *(short *)(param_1 + 0x16b0) =
               (short)((int)(uint)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f))
          ;
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar4;
        }
        else {
          *(ushort *)(param_1 + 0x16b0) =
               *(ushort *)(param_1 + 0x16b0) |
               *(short *)(param_3 + local_4c * 4) <<
               ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
          *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar4;
        }
        iVar3 = *(int *)(&DAT_00873368 + local_4c * 4);
        if (iVar3 != 0) {
          uVar5 = uVar5 - *(int *)(&DAT_00873cac + local_4c * 4);
          if (0x10 - iVar3 < *(int *)(param_1 + 0x16b4)) {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(uVar5 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)*(undefined2 *)(param_1 + 0x16b0);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
                 (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
            *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
            *(short *)(param_1 + 0x16b0) =
                 (short)((int)(uVar5 & 0xffff) >>
                        (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + iVar3;
          }
          else {
            *(ushort *)(param_1 + 0x16b0) =
                 *(ushort *)(param_1 + 0x16b0) |
                 (ushort)(uVar5 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
            *(int *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + iVar3;
          }
        }
      }
    } while (local_18 < *(uint *)(param_1 + 0x1698));
  }
  uVar5 = (uint)*(ushort *)(param_2 + 0x402);
  if ((int)(0x10 - uVar5) < *(int *)(param_1 + 0x16b4)) {
    uVar2 = *(ushort *)(param_2 + 0x400);
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) | uVar2 << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)*(undefined2 *)(param_1 + 0x16b0);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(char *)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x14)) =
         (char)((ushort)*(undefined2 *)(param_1 + 0x16b0) >> 8);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
    *(short *)(param_1 + 0x16b0) =
         (short)((int)(uint)uVar2 >> (0x10U - (char)*(undefined4 *)(param_1 + 0x16b4) & 0x1f));
    *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + -0x10 + uVar5;
  }
  else {
    *(ushort *)(param_1 + 0x16b0) =
         *(ushort *)(param_1 + 0x16b0) |
         *(short *)(param_2 + 0x400) << ((byte)*(undefined4 *)(param_1 + 0x16b4) & 0x1f);
    *(uint *)(param_1 + 0x16b4) = *(int *)(param_1 + 0x16b4) + uVar5;
  }
  *(uint *)(param_1 + 0x16ac) = (uint)*(ushort *)(param_2 + 0x402);
  return;
}

