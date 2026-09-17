
undefined4 FUN__text__0052f2b4(void)

{
  int iVar1;
  undefined4 uVar2;
  void *pvVar3;
  int *extraout_ECX;
  int iVar4;
  int *piVar5;
  int unaff_EBP;
  undefined4 *puVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  
  FUN__text__0057158c();
  if ((char)extraout_ECX[2] == '\x01') {
    iVar1 = extraout_ECX[1];
    iVar4 = *extraout_ECX;
    uVar8 = *(uint *)(iVar1 + 0x1058);
    uVar7 = *(uint *)(iVar4 + 0x1058);
    *(uint *)(unaff_EBP + -0x18) = uVar8;
    if (uVar8 <= uVar7) {
      *(uint *)(unaff_EBP + -0x18) = uVar7;
    }
    uVar8 = *(uint *)(iVar1 + 0x105c);
    uVar7 = *(uint *)(iVar4 + 0x105c);
    *(uint *)(unaff_EBP + -0x20) = uVar8;
    if (uVar7 <= uVar8) {
      *(uint *)(unaff_EBP + -0x20) = uVar7;
    }
    uVar8 = *(uint *)(iVar1 + 0x1060);
    uVar7 = *(uint *)(iVar4 + 0x1060);
    *(uint *)(unaff_EBP + -0x1c) = uVar8;
    if (uVar7 <= uVar8) {
      *(uint *)(unaff_EBP + -0x1c) = uVar7;
    }
    uVar8 = *(uint *)(unaff_EBP + -0x18);
    pvVar3 = (void *)FUN__text__00428a40(uVar8 << 4);
    *(void **)(unaff_EBP + -0x14) = pvVar3;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    if (pvVar3 == (void *)0x0) {
      *(undefined4 *)(unaff_EBP + -0x10) = 0;
    }
    else {
      _vector_constructor_iterator_
                (pvVar3,0x10,*(int *)(unaff_EBP + -0x18),
                 (_func_void_ptr_void_ptr *)&LAB__text__0052702e);
      *(undefined4 *)(unaff_EBP + -0x10) = *(undefined4 *)(unaff_EBP + -0x14);
    }
    *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
    if (*(int *)(unaff_EBP + -0x10) == 0) {
      uVar2 = 0x80004005;
    }
    else {
      iVar1 = *(int *)(extraout_ECX[1] + 0x1058);
      *(int *)(unaff_EBP + -0x18) = iVar1;
      pvVar3 = (void *)FUN__text__00428a40(iVar1 << 4);
      *(void **)(unaff_EBP + -0x14) = pvVar3;
      *(undefined4 *)(unaff_EBP + -4) = 1;
      if (pvVar3 == (void *)0x0) {
        *(undefined4 *)(unaff_EBP + -0x18) = 0;
      }
      else {
        _vector_constructor_iterator_
                  (pvVar3,0x10,*(int *)(unaff_EBP + -0x18),
                   (_func_void_ptr_void_ptr *)&LAB__text__0052702e);
        *(undefined4 *)(unaff_EBP + -0x18) = *(undefined4 *)(unaff_EBP + -0x14);
      }
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      if (*(int *)(unaff_EBP + -0x18) == 0) {
        FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x10));
        uVar2 = 0x80004005;
      }
      else {
        iVar1 = *(int *)(unaff_EBP + -0x1c);
        *(undefined4 *)(unaff_EBP + -0x14) = 0;
        puVar6 = *(undefined4 **)(unaff_EBP + -0x10);
        for (iVar4 = (uVar8 & 0xfffffff) << 2; iVar4 != 0; iVar4 = iVar4 + -1) {
          *puVar6 = 0;
          puVar6 = puVar6 + 1;
        }
        for (iVar4 = 0; iVar4 != 0; iVar4 = iVar4 + -1) {
          *(undefined1 *)puVar6 = 0;
          puVar6 = (undefined4 *)((int)puVar6 + 1);
        }
        puVar6 = *(undefined4 **)(unaff_EBP + -0x18);
        for (iVar4 = (*(uint *)(extraout_ECX[1] + 0x1058) & 0xfffffff) << 2; iVar4 != 0;
            iVar4 = iVar4 + -1) {
          *puVar6 = 0;
          puVar6 = puVar6 + 1;
        }
        for (iVar4 = 0; iVar4 != 0; iVar4 = iVar4 + -1) {
          *(undefined1 *)puVar6 = 0;
          puVar6 = (undefined4 *)((int)puVar6 + 1);
        }
        uVar8 = 0;
        if (iVar1 != 0) {
          do {
            uVar8 = *(uint *)(unaff_EBP + -0x20);
            uVar7 = 0;
            if (uVar8 != 0) {
              do {
                (**(code **)(*(int *)*extraout_ECX + 4))
                          (uVar7,*(undefined4 *)(unaff_EBP + -0x14),
                           *(undefined4 *)(unaff_EBP + -0x10));
                (**(code **)(*(int *)extraout_ECX[1] + 8))
                          (uVar7,*(undefined4 *)(unaff_EBP + -0x14),
                           *(undefined4 *)(unaff_EBP + -0x10));
                uVar7 = uVar7 + 1;
              } while (uVar7 < uVar8);
            }
            piVar5 = (int *)extraout_ECX[1];
            if (uVar8 < (uint)piVar5[0x417]) {
              do {
                (**(code **)(*piVar5 + 8))
                          (uVar8,*(undefined4 *)(unaff_EBP + -0x14),
                           *(undefined4 *)(unaff_EBP + -0x18));
                piVar5 = (int *)extraout_ECX[1];
                uVar8 = uVar8 + 1;
              } while (uVar8 < (uint)piVar5[0x417]);
            }
            uVar8 = *(uint *)(unaff_EBP + -0x1c);
            *(int *)(unaff_EBP + -0x14) = *(int *)(unaff_EBP + -0x14) + 1;
          } while (*(uint *)(unaff_EBP + -0x14) < uVar8);
        }
        piVar5 = (int *)extraout_ECX[1];
        if (uVar8 < (uint)piVar5[0x418]) {
          uVar7 = piVar5[0x417];
          do {
            uVar9 = 0;
            if (uVar7 != 0) {
              do {
                (**(code **)(*piVar5 + 8))(uVar9,uVar8,*(undefined4 *)(unaff_EBP + -0x18));
                piVar5 = (int *)extraout_ECX[1];
                uVar7 = piVar5[0x417];
                uVar9 = uVar9 + 1;
              } while (uVar9 < uVar7);
            }
            piVar5 = (int *)extraout_ECX[1];
            uVar8 = uVar8 + 1;
          } while (uVar8 < (uint)piVar5[0x418]);
        }
        FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x10));
        FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x18));
        uVar2 = 0;
      }
    }
  }
  else {
    uVar2 = 0x80004005;
  }
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar2;
}

