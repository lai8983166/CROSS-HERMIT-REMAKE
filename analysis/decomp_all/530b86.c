
undefined4 FUN__text__00530b86(void)

{
  int iVar1;
  uint uVar2;
  float fVar3;
  int *piVar4;
  int iVar5;
  void *pvVar6;
  int *extraout_ECX;
  int *piVar7;
  int *piVar8;
  float *pfVar9;
  int unaff_EBP;
  float *pfVar10;
  undefined4 uVar11;
  int *piVar12;
  undefined4 *puVar13;
  
  FUN__text__0057158c();
  iVar5 = extraout_ECX[1];
  iVar1 = *(int *)(iVar5 + 0x1060);
  *(undefined4 *)(unaff_EBP + -0x20) = 0;
  *(undefined4 *)(unaff_EBP + -0x34) = 0;
  *(undefined4 *)(unaff_EBP + -0x18) = 0;
  *(undefined4 *)(unaff_EBP + -0x3c) = 0;
  if ((iVar1 != 1) || (*(int *)(*extraout_ECX + 0x1060) != 1)) {
    uVar11 = 0x80004005;
    goto LAB__text__00530f19;
  }
  uVar2 = extraout_ECX[2];
  piVar4 = (int *)FUN__text__0052d6df(*(undefined4 *)(*extraout_ECX + 0x1058),
                                      *(undefined4 *)(iVar5 + 0x1058),~(uVar2 >> 0x10) & 1);
  *(int **)(unaff_EBP + -0x38) = piVar4;
  if (piVar4 == (int *)0x0) {
LAB__text__00530edb:
    uVar11 = 0x80004005;
  }
  else {
    iVar5 = FUN__text__0052d6df(*(undefined4 *)(*extraout_ECX + 0x105c),
                                *(undefined4 *)(extraout_ECX[1] + 0x105c),~(uVar2 >> 0x11) & 1);
    *(int *)(unaff_EBP + -0x20) = iVar5;
    if (iVar5 == 0) goto LAB__text__00530edb;
    *(int *)(unaff_EBP + -0x2c) = *piVar4 + (int)piVar4;
    piVar12 = (int *)(**(int **)(unaff_EBP + -0x20) + (int)*(int **)(unaff_EBP + -0x20));
    iVar5 = *(int *)(extraout_ECX[1] + 0x105c);
    *(int **)(unaff_EBP + -0x44) = piVar12;
    piVar4 = (int *)FUN__text__00428a40(iVar5 * 0xc + 4);
    *(int **)(unaff_EBP + -0x40) = piVar4;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    if (piVar4 == (int *)0x0) {
      *(undefined4 *)(unaff_EBP + -0x14) = 0;
      iVar5 = *(int *)(unaff_EBP + -0x14);
    }
    else {
      *piVar4 = iVar5;
      *(int **)(unaff_EBP + -0x34) = piVar4 + 1;
      _eh_vector_constructor_iterator_
                (piVar4 + 1,0xc,iVar5,(_func_void_void_ptr *)&LAB__text__0052d6c9,
                 (_func_void_void_ptr *)&LAB__text__0052d6d6);
      iVar5 = *(int *)(unaff_EBP + -0x34);
      *(int *)(unaff_EBP + -0x14) = iVar5;
    }
    *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
    *(int *)(unaff_EBP + -0x34) = iVar5;
    if (iVar5 == 0) {
LAB__text__00530ed4:
      uVar11 = 0x8007000e;
    }
    else {
      iVar5 = *(int *)(*extraout_ECX + 0x1058);
      pvVar6 = (void *)FUN__text__00428a40(iVar5 << 4);
      *(void **)(unaff_EBP + -0x3c) = pvVar6;
      *(undefined4 *)(unaff_EBP + -4) = 1;
      if (pvVar6 == (void *)0x0) {
        *(undefined4 *)(unaff_EBP + -0x24) = 0;
        iVar5 = *(int *)(unaff_EBP + -0x24);
      }
      else {
        _vector_constructor_iterator_
                  (pvVar6,0x10,iVar5,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
        iVar5 = *(int *)(unaff_EBP + -0x3c);
        *(int *)(unaff_EBP + -0x24) = iVar5;
      }
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      *(int *)(unaff_EBP + -0x3c) = iVar5;
      if (iVar5 == 0) goto LAB__text__00530ed4;
      piVar4 = (int *)(*(int *)(unaff_EBP + -0x20) + 4);
      *(int **)(unaff_EBP + -0x30) = piVar4;
      while (piVar4 < piVar12) {
        piVar8 = (int *)(*piVar4 + (int)piVar4);
        for (piVar7 = piVar4 + 1; piVar4 = piVar8, piVar7 < piVar8; piVar7 = piVar7 + 2) {
          piVar4 = (int *)(*(int *)(unaff_EBP + -0x14) + 8 + *piVar7 * 0xc);
          *piVar4 = *piVar4 + 1;
        }
      }
      piVar4 = *(int **)(unaff_EBP + -0x30);
      *(undefined4 *)(unaff_EBP + -0x28) = 0;
      if (piVar4 < piVar12) {
        do {
          iVar5 = *piVar4;
          piVar12 = piVar4 + 1;
          *(int **)(unaff_EBP + -0x1c) = (int *)(iVar5 + (int)piVar4);
          *(int **)(unaff_EBP + -0x30) = piVar12;
          piVar4 = (int *)(iVar5 + (int)piVar4);
          while (*(int **)(unaff_EBP + -0x10) = piVar12, piVar12 < piVar4) {
            piVar12 = (int *)(*(int *)(unaff_EBP + -0x14) + *piVar12 * 0xc);
            if (*piVar12 == 0) {
              piVar4 = *(int **)(unaff_EBP + -0x18);
              if (piVar4 == (int *)0x0) {
                iVar5 = *(int *)(extraout_ECX[1] + 0x1058);
                pvVar6 = (void *)FUN__text__00428a40(iVar5 << 4);
                *(void **)(unaff_EBP + -0x40) = pvVar6;
                *(undefined4 *)(unaff_EBP + -4) = 2;
                if (pvVar6 == (void *)0x0) {
                  iVar5 = 0;
                }
                else {
                  _vector_constructor_iterator_
                            (pvVar6,0x10,iVar5,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
                  iVar5 = *(int *)(unaff_EBP + -0x40);
                }
                *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
                *piVar12 = iVar5;
                if (iVar5 == 0) goto LAB__text__00530ed4;
              }
              else {
                *piVar12 = *piVar4;
                *piVar4 = 0;
                *(int *)(unaff_EBP + -0x18) = piVar4[1];
              }
              piVar4 = *(int **)(unaff_EBP + -0x1c);
              puVar13 = (undefined4 *)*piVar12;
              for (iVar5 = (*(uint *)(extraout_ECX[1] + 0x1058) & 0xfffffff) << 2; iVar5 != 0;
                  iVar5 = iVar5 + -1) {
                *puVar13 = 0;
                puVar13 = puVar13 + 1;
              }
              for (iVar5 = 0; iVar5 != 0; iVar5 = iVar5 + -1) {
                *(undefined1 *)puVar13 = 0;
                puVar13 = (undefined4 *)((int)puVar13 + 1);
              }
            }
            piVar12 = (int *)(*(int *)(unaff_EBP + -0x10) + 8);
          }
          iVar5 = *(int *)(unaff_EBP + -0x24);
          (**(code **)(*(int *)*extraout_ECX + 4))(*(undefined4 *)(unaff_EBP + -0x28),0,iVar5);
          piVar12 = (int *)(*(int *)(unaff_EBP + -0x38) + 4);
          if (piVar12 < *(int **)(unaff_EBP + -0x2c)) {
            pfVar9 = (float *)(iVar5 + 8);
            do {
              piVar7 = *(int **)(unaff_EBP + -0x30);
              piVar8 = (int *)(*piVar12 + (int)piVar12);
              *(int **)(unaff_EBP + -0x10) = piVar7;
              if (piVar7 < piVar4) {
                *(int **)(unaff_EBP + -0x40) = piVar12 + 1;
                while( true ) {
                  iVar5 = *(int *)(*(int *)(unaff_EBP + -0x14) + *piVar7 * 0xc);
                  piVar12 = *(int **)(unaff_EBP + -0x40);
                  if (piVar12 < piVar8) {
                    do {
                      fVar3 = (float)piVar12[1] * *(float *)(*(int *)(unaff_EBP + -0x10) + 4);
                      pfVar10 = (float *)(*piVar12 * 0x10 + iVar5);
                      *pfVar10 = fVar3 * pfVar9[-2] + *pfVar10;
                      pfVar10 = (float *)(*piVar12 * 0x10 + 4 + iVar5);
                      *pfVar10 = fVar3 * pfVar9[-1] + *pfVar10;
                      pfVar10 = (float *)(*piVar12 * 0x10 + 8 + iVar5);
                      *pfVar10 = fVar3 * *pfVar9 + *pfVar10;
                      pfVar10 = (float *)(*piVar12 * 0x10 + 0xc + iVar5);
                      piVar12 = piVar12 + 2;
                      *pfVar10 = fVar3 * pfVar9[1] + *pfVar10;
                    } while (piVar12 < piVar8);
                    piVar4 = *(int **)(unaff_EBP + -0x1c);
                  }
                  *(int *)(unaff_EBP + -0x10) = *(int *)(unaff_EBP + -0x10) + 8;
                  if (piVar4 <= *(int **)(unaff_EBP + -0x10)) break;
                  piVar7 = *(int **)(unaff_EBP + -0x10);
                }
              }
              pfVar9 = pfVar9 + 4;
              piVar12 = piVar8;
            } while (piVar8 < *(int **)(unaff_EBP + -0x2c));
          }
          piVar12 = *(int **)(unaff_EBP + -0x30);
          if (piVar12 < piVar4) {
            do {
              puVar13 = (undefined4 *)(*(int *)(unaff_EBP + -0x14) + *piVar12 * 0xc);
              piVar4 = puVar13 + 2;
              *piVar4 = *piVar4 + -1;
              if (*piVar4 == 0) {
                (**(code **)(*(int *)extraout_ECX[1] + 8))(*piVar12,0,*puVar13);
                puVar13[1] = *(undefined4 *)(unaff_EBP + -0x18);
                *(undefined4 **)(unaff_EBP + -0x18) = puVar13;
              }
              piVar12 = piVar12 + 2;
            } while (piVar12 < *(int **)(unaff_EBP + -0x1c));
            piVar4 = *(int **)(unaff_EBP + -0x1c);
          }
          *(int *)(unaff_EBP + -0x28) = *(int *)(unaff_EBP + -0x28) + 1;
        } while (piVar4 < *(int **)(unaff_EBP + -0x44));
      }
      uVar11 = 0;
    }
  }
  if (*(int *)(unaff_EBP + -0x34) != 0) {
    FUN__text__0052d99c(3);
  }
  FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x20));
  FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x38));
  FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x3c));
  FUN__text__00428ad0(0);
LAB__text__00530f19:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar11;
}

