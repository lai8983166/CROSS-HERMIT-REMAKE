
/* WARNING: Removing unreachable block (ram,0x0052d754) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int * FUN__text__0052d6df(uint param_1,int param_2,int param_3)

{
  int *piVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  int *piVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  uint uVar17;
  float local_24;
  uint local_1c;
  float local_18;
  uint local_10;
  float local_c;
  float local_8;
  
  uVar17 = 0;
  if ((param_1 != 0) && (param_2 != 0)) {
    fVar2 = (float)param_2;
    if (param_2 < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
    }
    fVar3 = (float)(int)param_1;
    if ((int)param_1 < 0) {
      fVar3 = fVar3 + _DAT_005d0a44;
    }
    fVar4 = fVar2 / fVar3;
    fVar5 = _DAT_005d0a3c / fVar4;
    if (param_1 != 0) {
      do {
        __ftol();
        uVar17 = uVar17 + 1;
      } while (uVar17 < param_1);
    }
    piVar10 = (int *)FUN__text__00428a40();
    if (piVar10 != (int *)0x0) {
      iVar14 = 0;
      local_1c = 0;
      iVar16 = 4;
      iVar15 = iVar16;
      if (param_1 != 0) {
        do {
          local_8 = 0.0;
          local_10 = 0;
          fVar6 = (float)(int)local_1c;
          iVar16 = iVar15 + 4;
          if ((int)local_1c < 0) {
            fVar6 = fVar6 + _DAT_005d0a44;
          }
          do {
            fVar7 = (float)(int)local_10;
            if ((int)local_10 < 0) {
              fVar7 = fVar7 + _DAT_005d0a44;
            }
            fVar7 = (fVar7 + fVar6) - _DAT_005d0a3c;
            local_24 = fVar7 * fVar4;
            local_c = fVar4 + local_24;
            if (param_3 == 0) {
              if (local_24 < _DAT_005d0a54) {
                local_24 = 0.0;
              }
              if (fVar2 < local_c) {
                local_c = fVar2;
              }
            }
            FUN__text__00571dc0((double)local_24);
            iVar11 = __ftol();
            fVar8 = (float)iVar11;
            if (fVar8 < local_c) {
              iVar12 = iVar11 - param_2;
              do {
                local_18 = _DAT_005d0a40 + fVar8;
                if (iVar11 < 0) {
                  iVar13 = iVar11 + param_2;
                }
                else {
                  iVar13 = iVar12;
                  if (iVar11 < param_2) {
                    iVar13 = iVar11;
                  }
                }
                if (iVar13 != iVar14) {
                  if (_DAT_005d0e08 < local_8) {
                    piVar1 = (int *)(iVar16 + (int)piVar10);
                    *piVar1 = iVar14;
                    iVar16 = iVar16 + 8;
                    piVar1[1] = (int)local_8;
                  }
                  local_8 = 0.0;
                  iVar14 = iVar13;
                }
                if (fVar8 < local_24) {
                  fVar8 = local_24;
                }
                if (local_c < local_18) {
                  local_18 = local_c;
                }
                if (param_3 == 0) {
                  if (_DAT_005d0a54 <= fVar7) {
                    if (fVar7 + _DAT_005d0a40 < fVar3) goto LAB__text__0052d906;
                    fVar9 = 0.0;
                  }
                  else {
                    fVar9 = 1.0;
                  }
                }
                else {
LAB__text__0052d906:
                  fVar9 = (local_18 + fVar8) * fVar5 - fVar7;
                }
                if (local_10 != 0) {
                  fVar9 = 1.0 - fVar9;
                }
                iVar11 = iVar11 + 1;
                iVar12 = iVar12 + 1;
                local_8 = (local_18 - fVar8) * fVar9 + local_8;
                fVar8 = (float)iVar11;
              } while (fVar8 < local_c);
            }
            local_10 = local_10 + 1;
          } while (local_10 < 2);
          if (_DAT_005d0e08 < local_8) {
            piVar1 = (int *)(iVar16 + (int)piVar10);
            iVar16 = iVar16 + 8;
            *piVar1 = iVar14;
            piVar1[1] = (int)local_8;
          }
          local_1c = local_1c + 1;
          *(int *)(iVar15 + (int)piVar10) = iVar16 - iVar15;
          iVar15 = iVar16;
        } while (local_1c < param_1);
      }
      *piVar10 = iVar16;
      return piVar10;
    }
  }
  return (int *)0x0;
}

