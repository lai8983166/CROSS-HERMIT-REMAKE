
/* WARNING (jumptable): Unable to track spacebase fully for stack */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__0052f6ba(void)

{
  int *piVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  int iVar6;
  undefined4 *puVar7;
  float fVar8;
  undefined4 uVar9;
  void *pvVar10;
  float *pfVar11;
  float *pfVar12;
  int *extraout_ECX;
  float *pfVar13;
  uint uVar14;
  int unaff_EBP;
  int iVar15;
  
  FUN__text__0057158c();
  if ((char)extraout_ECX[2] != '\x05') {
    uVar9 = 0x80004005;
    goto LAB__text__0052fab0;
  }
  iVar15 = *extraout_ECX;
  uVar14 = *(uint *)(iVar15 + 0x1058);
  iVar6 = extraout_ECX[1];
  if ((((*(uint *)(iVar6 + 0x1058) != uVar14 >> 1) &&
       ((*(uint *)(iVar6 + 0x1058) != 1 || (uVar14 != 1)))) ||
      ((*(uint *)(iVar6 + 0x105c) != *(uint *)(iVar15 + 0x105c) >> 1 &&
       ((*(uint *)(iVar6 + 0x105c) != 1 || (*(int *)(iVar15 + 0x105c) != 1)))))) ||
     ((*(int *)(iVar6 + 0x1060) != 1 || (*(int *)(iVar15 + 0x1060) != 1)))) {
    uVar9 = 0x80004005;
    goto LAB__text__0052fab0;
  }
  if ((1 < uVar14) && ((uVar14 & 1) != 0)) {
    *(uint *)(iVar15 + 0x1058) = uVar14 & 0xfffffffe;
    piVar1 = (int *)(*extraout_ECX + 0x1064);
    *piVar1 = *piVar1 - *(int *)(*extraout_ECX + 0x1068);
  }
  uVar14 = *(uint *)(*extraout_ECX + 0x105c);
  if (1 < uVar14) {
    *(uint *)(*extraout_ECX + 0x105c) = uVar14 & 0xfffffffe;
  }
  if ((*(byte *)((int)extraout_ECX + 10) & 8) == 0) {
    iVar15 = *extraout_ECX;
    iVar6 = *(int *)(iVar15 + 4);
    if (((iVar6 == *(int *)(extraout_ECX[1] + 4)) && (1 < *(uint *)(iVar15 + 0x1058))) &&
       (1 < *(uint *)(iVar15 + 0x105c))) {
      if (iVar6 < 0x1d) {
        if (iVar6 == 0x1c) {
LAB__text__0052f835:
          iVar15 = FUN__text__0052eaaa();
        }
        else {
          switch(iVar6) {
          default:
            goto switchD__text__0052f7c2_caseD_14;
          case 0x15:
            iVar15 = FUN__text__0052e136();
            break;
          case 0x16:
            iVar15 = FUN__text__0052e424();
            break;
          case 0x17:
            iVar15 = FUN__text__0052e455();
            break;
          case 0x18:
            iVar15 = FUN__text__0052e5a5();
            break;
          case 0x19:
            iVar15 = FUN__text__0052e6c9();
            break;
          case 0x1a:
            iVar15 = FUN__text__0052e818();
            break;
          case 0x1b:
            iVar15 = FUN__text__0052e96b();
          }
        }
      }
      else if (iVar6 == 0x1d) {
        iVar15 = FUN__text__0052eb45();
      }
      else if (iVar6 == 0x1e) {
        iVar15 = FUN__text__0052ec91();
      }
      else {
        if ((iVar6 == 0x28) || (iVar6 == 0x29)) goto switchD__text__0052f7c2_caseD_14;
        if (iVar6 == 0x32) goto LAB__text__0052f835;
        if (iVar6 == 0x33) {
          iVar15 = FUN__text__0052edbe();
        }
        else {
          if (iVar6 != 0x34) goto switchD__text__0052f7c2_caseD_14;
          iVar15 = FUN__text__0052ef0a();
        }
      }
      if (-1 < iVar15) {
        uVar9 = 0;
        goto LAB__text__0052fab0;
      }
    }
  }
switchD__text__0052f7c2_caseD_14:
  iVar15 = *(int *)(extraout_ECX[1] + 0x1058);
  pvVar10 = (void *)FUN__text__00428a40(iVar15 << 4);
  *(void **)(unaff_EBP + -0x2c) = pvVar10;
  *(undefined4 *)(unaff_EBP + -4) = 0;
  if (pvVar10 == (void *)0x0) {
    *(undefined4 *)(unaff_EBP + -0x1c) = 0;
  }
  else {
    _vector_constructor_iterator_
              (pvVar10,0x10,iVar15,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
    *(undefined4 *)(unaff_EBP + -0x1c) = *(undefined4 *)(unaff_EBP + -0x2c);
  }
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  if (*(int *)(unaff_EBP + -0x1c) == 0) {
    uVar9 = 0x8007000e;
  }
  else {
    iVar15 = *(int *)(*extraout_ECX + 0x1058);
    if (*(int *)(*extraout_ECX + 0x105c) == 1) {
      pvVar10 = (void *)FUN__text__00428a40(iVar15 << 4);
      *(void **)(unaff_EBP + -0x2c) = pvVar10;
      *(undefined4 *)(unaff_EBP + -4) = 1;
      if (pvVar10 == (void *)0x0) {
        iVar15 = 0;
      }
      else {
        _vector_constructor_iterator_
                  (pvVar10,0x10,iVar15,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
        iVar15 = *(int *)(unaff_EBP + -0x2c);
      }
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      *(int *)(unaff_EBP + -0x24) = iVar15;
      *(int *)(unaff_EBP + -0x14) = iVar15;
    }
    else {
      pvVar10 = (void *)FUN__text__00428a40(iVar15 << 5);
      *(void **)(unaff_EBP + -0x2c) = pvVar10;
      *(undefined4 *)(unaff_EBP + -4) = 2;
      if (pvVar10 == (void *)0x0) {
        iVar15 = 0;
      }
      else {
        _vector_constructor_iterator_
                  (pvVar10,0x10,iVar15 << 1,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
        iVar15 = *(int *)(unaff_EBP + -0x2c);
      }
      iVar6 = *(int *)(*extraout_ECX + 0x1058);
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      *(int *)(unaff_EBP + -0x24) = iVar15;
      *(int *)(unaff_EBP + -0x14) = iVar15;
      iVar15 = iVar6 * 0x10 + iVar15;
    }
    *(int *)(unaff_EBP + -0x10) = iVar15;
    if (*(int *)(unaff_EBP + -0x24) == 0) {
      uVar9 = 0x8007000e;
    }
    else {
      if (*(int *)(*extraout_ECX + 0x1058) == 1) {
        *(int *)(unaff_EBP + -0x28) = *(int *)(unaff_EBP + -0x14);
        iVar15 = *(int *)(unaff_EBP + -0x10);
      }
      else {
        *(int *)(unaff_EBP + -0x28) = *(int *)(unaff_EBP + -0x14) + 0x10;
        iVar15 = *(int *)(unaff_EBP + -0x10) + 0x10;
      }
      *(int *)(unaff_EBP + -0x2c) = iVar15;
      iVar15 = *(int *)(extraout_ECX[1] + 0x105c);
      *(undefined4 *)(unaff_EBP + -0x18) = 0;
      if (iVar15 != 0) {
        do {
          iVar15 = *(int *)(unaff_EBP + -0x14);
          iVar6 = *(int *)(unaff_EBP + -0x18) * 2;
          (**(code **)(*(int *)*extraout_ECX + 4))(iVar6,0,iVar15);
          if (*(int *)(unaff_EBP + -0x10) != iVar15) {
            (**(code **)(*(int *)*extraout_ECX + 4))(iVar6 + 1,0,*(undefined4 *)(unaff_EBP + -0x10))
            ;
          }
          fVar8 = _DAT_005d0e0c;
          uVar14 = 0;
          if (*(int *)(extraout_ECX[1] + 0x1058) != 0) {
            *(undefined4 *)(unaff_EBP + -0x20) = *(undefined4 *)(unaff_EBP + -0x1c);
            do {
              iVar15 = uVar14 * 0x20;
              pfVar11 = (float *)(*(int *)(unaff_EBP + -0x28) + iVar15);
              fVar2 = *pfVar11;
              pfVar13 = (float *)(*(int *)(unaff_EBP + -0x14) + iVar15);
              fVar3 = *pfVar13;
              puVar7 = *(undefined4 **)(unaff_EBP + -0x20);
              fVar4 = pfVar11[1];
              *(int *)(unaff_EBP + -0x20) = *(int *)(unaff_EBP + -0x20) + 0x10;
              fVar5 = pfVar13[1];
              *(float *)(unaff_EBP + -0x44) = pfVar11[2] + pfVar13[2];
              pfVar12 = (float *)(*(int *)(unaff_EBP + -0x10) + iVar15);
              *(float *)(unaff_EBP + -0x40) = pfVar11[3] + pfVar13[3];
              *(float *)(unaff_EBP + -0x5c) = fVar2 + fVar3 + *pfVar12;
              fVar2 = pfVar12[1];
              fVar3 = pfVar12[2];
              pfVar11 = (float *)(*(int *)(unaff_EBP + -0x2c) + iVar15);
              *(float *)(unaff_EBP + -0x50) = *(float *)(unaff_EBP + -0x40) + pfVar12[3];
              uVar14 = uVar14 + 1;
              *(float *)(unaff_EBP + -0x6c) = *(float *)(unaff_EBP + -0x5c) + *pfVar11;
              *(float *)(unaff_EBP + -0x68) = fVar4 + fVar5 + fVar2 + pfVar11[1];
              fVar2 = pfVar11[2];
              fVar4 = pfVar11[3];
              *(float *)(unaff_EBP + -0x3c) = *(float *)(unaff_EBP + -0x6c) * fVar8;
              *(float *)(unaff_EBP + -0x38) = *(float *)(unaff_EBP + -0x68) * fVar8;
              *(float *)(unaff_EBP + -0x34) =
                   (*(float *)(unaff_EBP + -0x44) + fVar3 + fVar2) * fVar8;
              *(float *)(unaff_EBP + -0x30) = (*(float *)(unaff_EBP + -0x50) + fVar4) * fVar8;
              *puVar7 = *(undefined4 *)(unaff_EBP + -0x3c);
              puVar7[1] = *(undefined4 *)(unaff_EBP + -0x38);
              puVar7[2] = *(undefined4 *)(unaff_EBP + -0x34);
              puVar7[3] = *(undefined4 *)(unaff_EBP + -0x30);
            } while (uVar14 < *(uint *)(extraout_ECX[1] + 0x1058));
          }
          (**(code **)(*(int *)extraout_ECX[1] + 8))
                    (*(undefined4 *)(unaff_EBP + -0x18),0,*(undefined4 *)(unaff_EBP + -0x1c));
          *(int *)(unaff_EBP + -0x18) = *(int *)(unaff_EBP + -0x18) + 1;
        } while (*(uint *)(unaff_EBP + -0x18) < *(uint *)(extraout_ECX[1] + 0x105c));
      }
      FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x24));
      uVar9 = 0;
    }
    FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x1c));
  }
LAB__text__0052fab0:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar9;
}

