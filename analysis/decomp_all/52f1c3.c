
undefined4 FUN__text__0052f1c3(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  void *pvVar4;
  uint uVar5;
  undefined4 uVar6;
  int *extraout_ECX;
  uint uVar7;
  int unaff_EBP;
  uint uVar8;
  
  FUN__text__0057158c();
  iVar1 = extraout_ECX[1];
  iVar2 = *extraout_ECX;
  iVar3 = *(int *)(iVar1 + 0x1058);
  if (((iVar3 == *(int *)(iVar2 + 0x1058)) && (*(int *)(iVar1 + 0x105c) == *(int *)(iVar2 + 0x105c))
      ) && (*(int *)(iVar1 + 0x1060) == *(int *)(iVar2 + 0x1060))) {
    pvVar4 = (void *)FUN__text__00428a40(iVar3 << 4);
    *(void **)(unaff_EBP + -0x10) = pvVar4;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    if (pvVar4 == (void *)0x0) {
      *(undefined4 *)(unaff_EBP + -0x10) = 0;
    }
    else {
      _vector_constructor_iterator_
                (pvVar4,0x10,iVar3,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
      *(void **)(unaff_EBP + -0x10) = pvVar4;
    }
    *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
    uVar7 = 0;
    if (*(int *)(unaff_EBP + -0x10) != 0) {
      if (*(int *)(extraout_ECX[1] + 0x1060) != 0) {
        uVar5 = *(uint *)(extraout_ECX[1] + 0x105c);
        do {
          uVar8 = 0;
          if (uVar5 != 0) {
            do {
              (**(code **)(*(int *)*extraout_ECX + 4))
                        (uVar8,uVar7,*(undefined4 *)(unaff_EBP + -0x10));
              (**(code **)(*(int *)extraout_ECX[1] + 8))
                        (uVar8,uVar7,*(undefined4 *)(unaff_EBP + -0x10));
              uVar5 = *(uint *)(extraout_ECX[1] + 0x105c);
              uVar8 = uVar8 + 1;
            } while (uVar8 < uVar5);
          }
          uVar7 = uVar7 + 1;
        } while (uVar7 < *(uint *)(extraout_ECX[1] + 0x1060));
      }
      FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x10));
      uVar6 = 0;
      goto LAB__text__0052f2a5;
    }
  }
  uVar6 = 0x80004005;
LAB__text__0052f2a5:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar6;
}

