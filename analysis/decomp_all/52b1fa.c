
undefined4 __thiscall FUN__text__0052b1fa(int *param_1,uint *param_2,uint param_3)

{
  uint *puVar1;
  byte bVar2;
  ushort uVar3;
  uint *puVar4;
  byte bVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  undefined1 *puVar9;
  uint uVar10;
  byte *pbVar11;
  byte *pbVar12;
  uint uVar13;
  uint uVar14;
  byte *pbVar15;
  byte *pbVar16;
  uint uVar17;
  byte *pbVar18;
  byte *pbVar19;
  byte *pbVar20;
  byte *pbVar21;
  int local_1c;
  byte *local_14;
  
  puVar4 = param_2;
  if (param_3 < 0x28) {
    return 0x80004005;
  }
  uVar17 = *param_2;
  if (uVar17 < 0x28) {
    return 0x80004005;
  }
  uVar14 = param_2[1];
  uVar6 = param_2[2];
  if ((int)uVar6 < 1) {
    uVar6 = -uVar6;
  }
  uVar3 = *(ushort *)((int)param_2 + 0xe);
  uVar7 = param_2[8];
  if ((uVar3 < 9) && (uVar7 == 0)) {
    uVar7 = 1 << ((byte)uVar3 & 0x1f);
  }
  uVar7 = uVar17 + uVar7 * 4;
  if (param_3 < uVar7) {
    return 0x80004005;
  }
  if ((short)param_2[3] != 1) {
    return 0x80004005;
  }
  if ((((int)param_2[2] < 0) && (param_2[4] != 0)) && (param_2[4] != 3)) {
    return 0x80004005;
  }
  if (param_2[4] < 3) {
    if (((uVar3 == 1) || (uVar3 == 4)) || (uVar3 == 8)) {
      param_3 = 0x29;
      goto LAB__text__0052b510;
    }
    if (uVar3 == 0x10) goto LAB__text__0052b500;
    if (uVar3 == 0x18) goto LAB__text__0052b3b0;
    if (uVar3 != 0x20) {
      return 0x80004005;
    }
  }
  else {
    if (param_2[4] != 3) {
      return 0x80004001;
    }
    if (uVar17 < 0x6c) {
      param_3 = 0;
      puVar1 = (uint *)(uVar17 + (int)param_2);
      uVar17 = puVar1[2];
      uVar10 = puVar1[1];
      uVar13 = *puVar1;
    }
    else {
      param_3 = param_2[0xd];
      uVar17 = param_2[0xc];
      uVar10 = param_2[0xb];
      uVar13 = param_2[10];
    }
    uVar3 = *(ushort *)((int)param_2 + 0xe);
    if (uVar3 == 0x10) {
      if (uVar17 == 0xff) {
        if (uVar10 != 0xff) {
          return 0x80004005;
        }
        if (uVar13 != 0xff) {
          return 0x80004005;
        }
        if (param_3 != 0xff00) {
          return 0x80004005;
        }
        param_3 = 0x33;
        goto LAB__text__0052b510;
      }
      if (uVar17 != 0x1f) {
        if (uVar17 == 0xf) {
          if (uVar10 != 0xf0) {
            return 0x80004005;
          }
          if (uVar13 != 0xf00) {
            return 0x80004005;
          }
          if (param_3 == 0xf000) {
            param_3 = 0x1a;
          }
          else {
            if (param_3 != 0) {
              return 0x80004005;
            }
            param_3 = 0x1e;
          }
        }
        else {
          if (uVar17 != 3) {
            return 0x80004005;
          }
          if (uVar10 != 0x1c) {
            return 0x80004005;
          }
          if (uVar13 != 0xe0) {
            return 0x80004005;
          }
          if (param_3 != 0xff00) {
            return 0x80004005;
          }
          param_3 = 0x1d;
        }
        goto LAB__text__0052b510;
      }
      if (uVar10 == 0x7e0) {
        if (uVar13 != 0xf800) {
          return 0x80004005;
        }
        if (param_3 != 0) {
          return 0x80004005;
        }
        param_3 = 0x17;
        goto LAB__text__0052b510;
      }
      if (uVar10 != 0x3e0) {
        return 0x80004005;
      }
      if (uVar13 != 0x7c00) {
        return 0x80004005;
      }
      if (param_3 != 0) {
        if (param_3 != 0x8000) {
          return 0x80004005;
        }
        param_3 = 0x19;
        goto LAB__text__0052b510;
      }
LAB__text__0052b500:
      param_3 = 0x18;
      goto LAB__text__0052b510;
    }
    if (uVar3 == 0x18) {
      if (uVar17 != 0xff) {
        return 0x80004005;
      }
      if (uVar10 != 0xff00) {
        return 0x80004005;
      }
      if (uVar13 != 0xff0000) {
        return 0x80004005;
      }
      if (param_3 != 0) {
        return 0x80004005;
      }
LAB__text__0052b3b0:
      param_3 = 0x14;
      goto LAB__text__0052b510;
    }
    if (uVar3 != 0x20) {
      return 0x80004005;
    }
    if (uVar17 != 0xff) {
      if (uVar17 == 0x3ff00000) {
        if (uVar10 != 0xffc00) {
          return 0x80004005;
        }
        if (uVar13 != 0x3ff) {
          return 0x80004005;
        }
        if (param_3 != 0xc0000000) {
          return 0x80004005;
        }
        param_3 = 0x1f;
      }
      else {
        if (uVar17 != 0) {
          return 0x80004005;
        }
        if (uVar10 != 0xffff0000) {
          return 0x80004005;
        }
        if (uVar13 != 0xffff) {
          return 0x80004005;
        }
        if (param_3 != 0) {
          return 0x80004005;
        }
        param_3 = 0x22;
      }
      goto LAB__text__0052b510;
    }
    if (uVar10 != 0xff00) {
      return 0x80004005;
    }
    if (uVar13 != 0xff0000) {
      return 0x80004005;
    }
    if (param_3 != 0) {
      if (param_3 != 0xff000000) {
        return 0x80004005;
      }
      param_3 = 0x15;
      goto LAB__text__0052b510;
    }
  }
  param_3 = 0x16;
LAB__text__0052b510:
  if ((param_1[0x10] != 0) && (param_3 == 0x29)) {
    uVar17 = param_2[8];
    if (uVar17 == 0) {
      uVar17 = 1 << ((byte)uVar3 & 0x1f);
    }
    param_1[0xf] = 1;
    iVar8 = FUN__text__00428a40(0x400);
    param_1[2] = iVar8;
    if (iVar8 == 0) {
      return 0x8007000e;
    }
    uVar10 = *param_2;
    param_2 = (uint *)0x0;
    puVar9 = (undefined1 *)(uVar10 + (int)puVar4);
    if (uVar17 != 0) {
      do {
        iVar8 = (int)param_2 * 4;
        *(undefined1 *)(iVar8 + param_1[2]) = puVar9[2];
        *(undefined1 *)(iVar8 + 1 + param_1[2]) = puVar9[1];
        *(undefined1 *)(iVar8 + 2 + param_1[2]) = *puVar9;
        *(undefined1 *)(iVar8 + 3 + param_1[2]) = 0xff;
        param_2 = (uint *)((int)param_2 + 1);
        puVar9 = puVar9 + 4;
      } while (param_2 < uVar17);
    }
    for (; uVar17 < 0x100; uVar17 = uVar17 + 1) {
      iVar8 = uVar17 * 4;
      *(undefined1 *)(iVar8 + param_1[2]) = 0xff;
      *(undefined1 *)(iVar8 + 1 + param_1[2]) = 0xff;
      *(undefined1 *)(iVar8 + 2 + param_1[2]) = 0xff;
      *(undefined1 *)(iVar8 + 3 + param_1[2]) = 0xff;
    }
  }
  uVar3 = *(ushort *)((int)puVar4 + 0xe);
  uVar17 = uVar14;
  if (uVar3 == 1) {
    uVar10 = uVar14 + 7 >> 3;
  }
  else if (uVar3 == 4) {
    uVar10 = uVar14 + 1 >> 1;
  }
  else {
    uVar10 = (uVar3 >> 3) * uVar14;
    uVar17 = uVar10;
  }
  uVar13 = uVar10 + 3 & 0xfffffffc;
  *param_1 = param_3;
  uVar10 = uVar17 + 3 & 0xfffffffc;
  param_1[3] = uVar14;
  param_1[0xc] = uVar10;
  param_1[0xd] = 0;
  param_1[4] = uVar6;
  param_1[5] = 1;
  if (param_1[0x10] != 0) {
    if (((int)puVar4[2] < 0) && (7 < *(ushort *)((int)puVar4 + 0xe))) {
      param_1[0xe] = 0;
      param_1[1] = uVar7 + (int)puVar4;
    }
    else {
      param_1[0xe] = 1;
      pbVar11 = (byte *)FUN__text__00428a40(uVar10 * uVar6);
      param_1[1] = (int)pbVar11;
      if (pbVar11 == (byte *)0x0) {
        return 0x8007000e;
      }
      pbVar15 = (byte *)(uVar7 + (int)puVar4);
      iVar8 = param_1[0xc];
      pbVar18 = pbVar11;
      local_1c = iVar8;
      if (-1 < (int)puVar4[2]) {
        pbVar18 = pbVar11 + (uVar6 - 1) * iVar8;
        local_1c = -iVar8;
      }
      pbVar12 = pbVar11 + iVar8 * uVar6;
      local_14 = pbVar18;
      if (puVar4[4] == 2) {
        while (pbVar11 <= pbVar18) {
          if (*pbVar15 == 0) {
            bVar5 = pbVar15[1];
            if (bVar5 == 0) {
              pbVar18 = local_14 + -param_1[0xc];
              local_14 = pbVar18;
            }
            else if (bVar5 == 1) {
              pbVar18 = pbVar11 + -param_1[0xc];
            }
            else if (bVar5 == 2) {
              pbVar12 = pbVar15 + 3;
              pbVar15 = pbVar15 + 2;
              pbVar18 = pbVar18 + ((uint)*pbVar15 - (uint)*pbVar12 * param_1[0xc]);
            }
            else {
              uVar17 = 0;
              if (bVar5 != 0) {
                do {
                  if ((uVar17 & 1) == 0) {
                    bVar5 = pbVar15[((int)uVar17 >> 1) + 2] >> 4;
                  }
                  else {
                    bVar5 = pbVar15[((int)uVar17 >> 1) + 2] & 0xf;
                  }
                  pbVar18[uVar17] = bVar5;
                  uVar17 = uVar17 + 1;
                } while ((int)uVar17 < (int)(uint)pbVar15[1]);
              }
              pbVar18 = pbVar18 + pbVar15[1];
              pbVar15 = pbVar15 + ((pbVar15[1] >> 1) + 1 & 0xfffffffe);
            }
          }
          else {
            uVar17 = 0;
            if (*pbVar15 != 0) {
              do {
                if ((uVar17 & 1) == 0) {
                  bVar5 = pbVar15[1] >> 4;
                }
                else {
                  bVar5 = pbVar15[1] & 0xf;
                }
                pbVar18[uVar17] = bVar5;
                uVar17 = uVar17 + 1;
              } while ((int)uVar17 < (int)(uint)*pbVar15);
            }
            pbVar18 = pbVar18 + *pbVar15;
          }
          pbVar15 = pbVar15 + 2;
        }
      }
      else if (puVar4[4] == 1) {
        while (pbVar11 <= pbVar18) {
          bVar5 = *pbVar15;
          if (bVar5 == 0) {
            uVar17 = (uint)pbVar15[1];
            if (uVar17 == 0) {
              pbVar18 = local_14 + -param_1[0xc];
              local_14 = pbVar18;
            }
            else if (uVar17 == 1) {
              pbVar18 = pbVar11 + -param_1[0xc];
            }
            else {
              if (uVar17 != 2) {
                pbVar12 = pbVar15 + 2;
                pbVar16 = pbVar18;
                for (uVar14 = (uint)(pbVar15[1] >> 2); uVar14 != 0; uVar14 = uVar14 - 1) {
                  *(undefined4 *)pbVar16 = *(undefined4 *)pbVar12;
                  pbVar12 = pbVar12 + 4;
                  pbVar16 = pbVar16 + 4;
                }
                for (uVar17 = uVar17 & 3; uVar17 != 0; uVar17 = uVar17 - 1) {
                  *pbVar16 = *pbVar12;
                  pbVar12 = pbVar12 + 1;
                  pbVar16 = pbVar16 + 1;
                }
                uVar17 = (uint)pbVar15[1];
                pbVar15 = pbVar15 + (uVar17 + 1 & 0xfffffffe);
                goto LAB__text__0052b810;
              }
              pbVar12 = pbVar15 + 3;
              pbVar15 = pbVar15 + 2;
              pbVar18 = pbVar18 + ((uint)*pbVar15 - (uint)*pbVar12 * param_1[0xc]);
            }
          }
          else {
            bVar2 = pbVar15[1];
            pbVar12 = pbVar18;
            for (uVar17 = (uint)(bVar5 >> 2); uVar17 != 0; uVar17 = uVar17 - 1) {
              *(uint *)pbVar12 = CONCAT22(CONCAT11(bVar2,bVar2),CONCAT11(bVar2,bVar2));
              pbVar12 = pbVar12 + 4;
            }
            for (uVar17 = bVar5 & 3; uVar17 != 0; uVar17 = uVar17 - 1) {
              *pbVar12 = bVar2;
              pbVar12 = pbVar12 + 1;
            }
            uVar17 = (uint)*pbVar15;
LAB__text__0052b810:
            pbVar18 = pbVar18 + uVar17;
          }
          pbVar15 = pbVar15 + 2;
        }
      }
      else if (*(short *)((int)puVar4 + 0xe) == 1) {
        for (; (pbVar11 <= pbVar18 && (pbVar18 < pbVar12)); pbVar18 = pbVar18 + local_1c) {
          param_2 = (uint *)0x0;
          if (uVar14 != 0) {
            do {
              pbVar18[(int)param_2] =
                   pbVar15[(uint)param_2 >> 3] >> (7 - ((byte)param_2 & 7) & 0x1f) & 1;
              param_2 = (uint *)((int)param_2 + 1);
            } while (param_2 < uVar14);
          }
          pbVar15 = pbVar15 + uVar13;
        }
      }
      else if (*(short *)((int)puVar4 + 0xe) == 4) {
        for (; (pbVar11 <= pbVar18 && (pbVar18 < pbVar12)); pbVar18 = pbVar18 + local_1c) {
          uVar17 = 0;
          if (uVar14 != 0) {
            do {
              if ((uVar17 & 1) == 0) {
                bVar5 = pbVar15[uVar17 >> 1] >> 4;
              }
              else {
                bVar5 = pbVar15[uVar17 >> 1] & 0xf;
              }
              pbVar18[uVar17] = bVar5;
              uVar17 = uVar17 + 1;
            } while (uVar17 < uVar14);
          }
          pbVar15 = pbVar15 + uVar13;
        }
      }
      else {
        while ((pbVar11 <= pbVar18 && (pbVar18 < pbVar12))) {
          pbVar16 = pbVar15 + uVar13;
          pbVar19 = pbVar18 + local_1c;
          for (uVar14 = uVar17 >> 2; uVar14 != 0; uVar14 = uVar14 - 1) {
            *(undefined4 *)pbVar18 = *(undefined4 *)pbVar15;
            pbVar15 = pbVar15 + 4;
            pbVar18 = pbVar18 + 4;
          }
          pbVar20 = pbVar15;
          pbVar21 = pbVar18;
          for (uVar14 = uVar17 & 3; pbVar15 = pbVar16, pbVar18 = pbVar19, uVar14 != 0;
              uVar14 = uVar14 - 1) {
            *pbVar21 = *pbVar20;
            pbVar20 = pbVar20 + 1;
            pbVar21 = pbVar21 + 1;
          }
        }
      }
    }
  }
  return 0;
}

