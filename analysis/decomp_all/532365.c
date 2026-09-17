
undefined4 FUN__text__00532365(void)

{
  int iVar1;
  void *pvVar2;
  void *pvVar3;
  undefined4 uVar4;
  int extraout_ECX;
  int unaff_EBP;
  
  FUN__text__0057158c();
  if (*(int *)(extraout_ECX + 8) != *(int *)(*(int *)(unaff_EBP + 8) + 8)) {
    iVar1 = *(int *)(extraout_ECX + 0x1058);
    pvVar2 = (void *)FUN__text__00428a40(iVar1 << 4);
    *(void **)(unaff_EBP + -0x10) = pvVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    pvVar3 = (void *)0x0;
    if (pvVar2 != (void *)0x0) {
      _vector_constructor_iterator_
                (pvVar2,0x10,iVar1,(_func_void_ptr_void_ptr *)&LAB__text__0052702e);
      pvVar3 = pvVar2;
    }
    *(void **)(extraout_ECX + 0x104c) = pvVar3;
    if (pvVar3 == (void *)0x0) {
      uVar4 = 0x8007000e;
      goto LAB__text__005323d1;
    }
    *(undefined4 *)(extraout_ECX + 0x1048) = *(undefined4 *)(*(int *)(unaff_EBP + 8) + 8);
  }
  uVar4 = 0;
LAB__text__005323d1:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar4;
}

