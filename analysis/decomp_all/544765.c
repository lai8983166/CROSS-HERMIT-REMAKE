
void FUN__text__00544765(int param_1,byte *param_2,uint param_3,uint param_4,int param_5,int param_6
                        )

{
  undefined2 uVar1;
  byte bVar2;
  byte bVar3;
  undefined4 *puVar4;
  bool bVar5;
  undefined4 uVar6;
  int iVar7;
  byte *pbVar8;
  byte *pbVar9;
  byte *pbVar10;
  uint uVar11;
  uint uVar12;
  int *piVar13;
  undefined4 *puVar14;
  undefined4 *puVar15;
  int iVar16;
  int iVar17;
  int iVar18;
  uint uVar19;
  uint uVar20;
  uint uVar21;
  uint uVar22;
  byte *pbVar23;
  uint local_2c;
  uint local_28;
  uint local_24;
  int local_1c;
  int local_18;
  byte *local_14;
  int local_10;
  uint local_c;
  
  *(uint *)(param_1 + 0x60) = *(uint *)(param_1 + 0x60) | 0x40;
  if (param_6 == 0) {
    uVar6 = FUN__text__0054bc20(param_1,param_3);
    *(undefined4 *)(param_1 + 0x178) = uVar6;
    iVar7 = 0;
    if (0 < (int)param_3) {
      do {
        *(char *)(iVar7 + *(int *)(param_1 + 0x178)) = (char)iVar7;
        iVar7 = iVar7 + 1;
      } while (iVar7 < (int)param_3);
    }
  }
  if ((int)param_4 < (int)param_3) {
    pbVar8 = (byte *)FUN__text__0054bc20(param_1,param_3);
    if (param_5 == 0) {
      iVar7 = FUN__text__0054bc20(param_1,param_3);
      iVar16 = 0;
      if (0 < (int)param_3) {
        do {
          ((undefined1 *)(iVar16 + iVar7))[(int)pbVar8 - iVar7] = (char)iVar16;
          *(undefined1 *)(iVar16 + iVar7) = (char)iVar16;
          iVar16 = iVar16 + 1;
        } while (iVar16 < (int)param_3);
      }
      puVar15 = (undefined4 *)FUN__text__0054bc20(param_1,0xc04);
      puVar14 = puVar15;
      for (iVar16 = 0x301; iVar16 != 0; iVar16 = iVar16 + -1) {
        *puVar14 = 0;
        puVar14 = puVar14 + 1;
      }
      local_10 = 0x60;
      uVar22 = param_3;
      do {
        local_c = 0;
        if (uVar22 != 1 && -1 < (int)(uVar22 - 1)) {
          pbVar10 = param_2 + 2;
          do {
            iVar16 = local_c + 1;
            if (iVar16 < (int)uVar22) {
              pbVar9 = pbVar10 + 2;
              local_14 = (byte *)iVar16;
              do {
                uVar11 = (int)((uint)pbVar10[-2] - (uint)pbVar9[-1]) >> 0x1f;
                uVar12 = (int)((uint)*pbVar10 - (uint)pbVar9[1]) >> 0x1f;
                uVar19 = (int)((uint)pbVar10[-1] - (uint)*pbVar9) >> 0x1f;
                iVar18 = (((uint)pbVar10[-2] - (uint)pbVar9[-1] ^ uVar11) - uVar11) +
                         (((uint)*pbVar10 - (uint)pbVar9[1] ^ uVar12) - uVar12) +
                         (((uint)pbVar10[-1] - (uint)*pbVar9 ^ uVar19) - uVar19);
                if (iVar18 <= local_10) {
                  puVar14 = (undefined4 *)FUN__text__0054bc20(param_1,8);
                  *puVar14 = puVar15[iVar18];
                  *(undefined1 *)(puVar14 + 1) = (undefined1)local_c;
                  *(undefined1 *)((int)puVar14 + 5) = local_14._0_1_;
                  puVar15[iVar18] = puVar14;
                }
                local_14 = (byte *)((int)local_14 + 1);
                pbVar9 = pbVar9 + 3;
              } while ((int)local_14 < (int)uVar22);
            }
            pbVar10 = pbVar10 + 3;
            local_c = iVar16;
          } while (iVar16 < (int)(uVar22 - 1));
        }
        local_c = 0;
        if (-1 < local_10) {
          do {
            piVar13 = (int *)puVar15[local_c];
            if (piVar13 != (int *)0x0) {
              pbVar10 = param_2 + uVar22 * 3;
              do {
                local_2c = (uint)*(byte *)(piVar13 + 1);
                pbVar9 = pbVar10;
                if (((int)(uint)pbVar8[local_2c] < (int)uVar22) &&
                   (uVar11 = (uint)*(byte *)((int)piVar13 + 5),
                   (int)(uint)pbVar8[uVar11] < (int)uVar22)) {
                  uVar12 = uVar11;
                  if ((uVar22 & 1) != 0) {
                    uVar12 = local_2c;
                    local_2c = uVar11;
                  }
                  pbVar23 = pbVar8 + uVar12;
                  bVar2 = *pbVar23;
                  pbVar9 = pbVar10 + -3;
                  *(undefined2 *)(param_2 + (uint)bVar2 * 3) = *(undefined2 *)pbVar9;
                  (param_2 + (uint)bVar2 * 3)[2] = pbVar10[-1];
                  iVar16 = 0;
                  uVar22 = uVar22 - 1;
                  if ((param_6 == 0) && (0 < (int)param_3)) {
                    do {
                      pbVar10 = (byte *)(*(int *)(param_1 + 0x178) + iVar16);
                      if (*pbVar10 == *pbVar23) {
                        *pbVar10 = pbVar8[local_2c];
                      }
                      pbVar10 = (byte *)(*(int *)(param_1 + 0x178) + iVar16);
                      if (*pbVar10 == uVar22) {
                        *pbVar10 = *pbVar23;
                      }
                      iVar16 = iVar16 + 1;
                    } while (iVar16 < (int)param_3);
                  }
                  pbVar8[*(byte *)(uVar22 + iVar7)] = *pbVar23;
                  *(undefined1 *)((uint)*pbVar23 + iVar7) = *(undefined1 *)(uVar22 + iVar7);
                  *pbVar23 = (byte)uVar22;
                  local_28._0_1_ = (undefined1)uVar12;
                  *(undefined1 *)(uVar22 + iVar7) = (undefined1)local_28;
                }
                if ((int)uVar22 <= (int)param_4) goto LAB__text__00544be1;
                piVar13 = (int *)*piVar13;
                pbVar10 = pbVar9;
              } while (piVar13 != (int *)0x0);
              if ((int)uVar22 <= (int)param_4) break;
            }
            local_c = local_c + 1;
          } while ((int)local_c <= local_10);
        }
LAB__text__00544be1:
        local_c = 0;
        do {
          puVar14 = (undefined4 *)puVar15[local_c];
          while (puVar14 != (undefined4 *)0x0) {
            puVar4 = (undefined4 *)*puVar14;
            FUN__text__0054bc56(param_1,puVar14);
            puVar14 = puVar4;
          }
          puVar15[local_c] = 0;
          local_c = local_c + 1;
        } while ((int)local_c < 0x301);
        local_10 = local_10 + 0x60;
      } while ((int)param_4 < (int)uVar22);
      FUN__text__0054bc56(param_1,puVar15);
      FUN__text__0054bc56(param_1,iVar7);
      FUN__text__0054bc56(param_1,pbVar8);
    }
    else {
      iVar7 = 0;
      if (0 < (int)param_3) {
        do {
          pbVar8[iVar7] = (byte)iVar7;
          iVar7 = iVar7 + 1;
        } while (iVar7 < (int)param_3);
      }
      iVar7 = param_3 - 1;
      if ((int)param_4 <= iVar7) {
        while (bVar5 = true, pbVar10 = pbVar8, local_2c = iVar7, 0 < iVar7) {
          do {
            pbVar9 = pbVar10 + 1;
            bVar2 = *pbVar10;
            if (*(ushort *)(param_5 + (uint)bVar2 * 2) < *(ushort *)(param_5 + (uint)*pbVar9 * 2)) {
              bVar5 = false;
              *pbVar10 = *pbVar9;
              *pbVar9 = bVar2;
            }
            local_2c = local_2c + -1;
            pbVar10 = pbVar9;
          } while (local_2c != 0);
          if ((bVar5) || (iVar7 = iVar7 + -1, iVar7 < (int)param_4)) break;
        }
      }
      iVar7 = 0;
      if (param_6 == 0) {
        iVar7 = 0;
        if (0 < (int)param_4) {
          local_14 = param_2;
          uVar22 = param_3;
          do {
            if ((int)param_4 <= (int)(uint)pbVar8[iVar7]) {
              do {
                uVar22 = uVar22 - 1;
              } while ((int)param_4 <= (int)(uint)pbVar8[uVar22]);
              pbVar10 = param_2 + uVar22 * 3;
              uVar1 = *(undefined2 *)pbVar10;
              bVar2 = pbVar10[2];
              *(undefined2 *)pbVar10 = *(undefined2 *)local_14;
              pbVar10[2] = local_14[2];
              *(undefined2 *)local_14 = uVar1;
              local_14[2] = bVar2;
              *(char *)(uVar22 + *(int *)(param_1 + 0x178)) = (char)iVar7;
              *(char *)(iVar7 + *(int *)(param_1 + 0x178)) = (char)uVar22;
            }
            local_14 = local_14 + 3;
            iVar7 = iVar7 + 1;
          } while (iVar7 < (int)param_4);
        }
        local_c = 0;
        if (0 < (int)param_3) {
          do {
            pbVar10 = (byte *)(*(int *)(param_1 + 0x178) + local_c);
            uVar22 = (uint)*pbVar10;
            if ((int)param_4 <= (int)uVar22) {
              pbVar9 = param_2 + uVar22 * 3;
              uVar22 = (uint)pbVar9[1] - (uint)param_2[1];
              uVar19 = (int)uVar22 >> 0x1f;
              local_2c = 0;
              local_2c._0_1_ = 0;
              uVar11 = (uint)pbVar9[2] - (uint)param_2[2];
              uVar20 = (int)uVar11 >> 0x1f;
              uVar12 = (uint)*pbVar9 - (uint)*param_2;
              uVar21 = (int)uVar12 >> 0x1f;
              iVar7 = ((uVar22 ^ uVar19) - uVar19) + ((uVar11 ^ uVar20) - uVar20) +
                      ((uVar12 ^ uVar21) - uVar21);
              local_14 = (byte *)0x1;
              if (1 < (int)param_4) {
                pbVar23 = param_2 + 4;
                do {
                  uVar22 = (uint)*pbVar9 - (uint)pbVar23[-1];
                  uVar19 = (int)uVar22 >> 0x1f;
                  uVar11 = (uint)pbVar9[2] - (uint)pbVar23[1];
                  uVar20 = (int)uVar11 >> 0x1f;
                  uVar12 = (uint)pbVar9[1] - (uint)*pbVar23;
                  uVar21 = (int)uVar12 >> 0x1f;
                  iVar16 = ((uVar22 ^ uVar19) - uVar19) + ((uVar11 ^ uVar20) - uVar20) +
                           ((uVar12 ^ uVar21) - uVar21);
                  if (iVar16 < iVar7) {
                    local_2c = (uint)local_14;
                    iVar7 = iVar16;
                  }
                  local_14 = (byte *)((int)local_14 + 1);
                  pbVar23 = pbVar23 + 3;
                } while ((int)local_14 < (int)param_4);
              }
              *pbVar10 = (byte)local_2c;
            }
            local_c = local_c + 1;
          } while ((int)local_c < (int)param_3);
        }
      }
      else {
        pbVar10 = param_2;
        if (0 < (int)param_4) {
          do {
            if ((int)param_4 <= (int)(uint)pbVar8[iVar7]) {
              do {
                param_3 = param_3 - 1;
              } while ((int)param_4 <= (int)(uint)pbVar8[param_3]);
              *(undefined2 *)pbVar10 = *(undefined2 *)(param_2 + param_3 * 3);
              pbVar10[2] = (param_2 + param_3 * 3)[2];
            }
            iVar7 = iVar7 + 1;
            pbVar10 = pbVar10 + 3;
          } while (iVar7 < (int)param_4);
        }
      }
      FUN__text__0054bc56(param_1,pbVar8);
    }
    param_3 = param_4;
  }
  if (*(int *)(param_1 + 0x104) == 0) {
    *(int *)(param_1 + 0x104) = (int)param_2;
  }
  *(short *)(param_1 + 0x108) = (short)param_3;
  if (param_6 != 0) {
    puVar14 = (undefined4 *)FUN__text__0054bc20(param_1,0x8000);
    *(undefined4 **)(param_1 + 0x174) = puVar14;
    for (iVar7 = 0x2000; iVar7 != 0; iVar7 = iVar7 + -1) {
      *puVar14 = 0;
      puVar14 = puVar14 + 1;
    }
    puVar15 = (undefined4 *)FUN__text__0054bc20(param_1,0x8000);
    local_18 = 0;
    puVar14 = puVar15;
    for (iVar7 = 0x2000; iVar7 != 0; iVar7 = iVar7 + -1) {
      *puVar14 = 0xffffffff;
      puVar14 = puVar14 + 1;
    }
    if (0 < (int)param_3) {
      param_2 = param_2 + 2;
      do {
        bVar2 = param_2[-1];
        bVar3 = *param_2;
        local_1c = 0;
        local_28 = -(uint)(param_2[-2] >> 3);
        do {
          iVar7 = (local_28 ^ (int)local_28 >> 0x1f) - ((int)local_28 >> 0x1f);
          param_6 = 0;
          local_24 = -(uint)(bVar2 >> 3);
          do {
            iVar16 = (local_24 ^ (int)local_24 >> 0x1f) - ((int)local_24 >> 0x1f);
            local_10 = iVar7;
            if (iVar7 <= iVar16) {
              local_10 = iVar16;
            }
            param_4 = 0;
            local_c = -(uint)(bVar3 >> 3);
            do {
              iVar17 = (local_c ^ (int)local_c >> 0x1f) - ((int)local_c >> 0x1f);
              uVar22 = param_4 | param_6 << 5 | local_1c << 10;
              iVar18 = local_10;
              if (local_10 <= iVar17) {
                iVar18 = iVar17;
              }
              iVar18 = iVar17 + iVar18 + iVar16 + iVar7;
              if (iVar18 < (int)(uint)*(byte *)(uVar22 + (int)puVar15)) {
                *(char *)(uVar22 + (int)puVar15) = (char)iVar18;
                *(undefined1 *)(uVar22 + *(int *)(param_1 + 0x174)) = (undefined1)local_18;
              }
              param_4 = param_4 + 1;
              local_c = local_c + 1;
            } while ((int)param_4 < 0x20);
            param_6 = param_6 + 1;
            local_24 = local_24 + 1;
          } while (param_6 < 0x20);
          local_1c = local_1c + 1;
          local_28 = local_28 + 1;
        } while (local_1c < 0x20);
        local_18 = local_18 + 1;
        param_2 = param_2 + 3;
      } while (local_18 < (int)param_3);
    }
    FUN__text__0054bc56(param_1,puVar15);
  }
  return;
}

