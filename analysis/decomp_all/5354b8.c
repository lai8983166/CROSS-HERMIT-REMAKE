
undefined4 * FUN__text__005354b8(void)

{
  uint uVar1;
  uint uVar2;
  void *pvVar3;
  undefined4 *extraout_ECX;
  int iVar4;
  int unaff_EBP;
  
  FUN__text__0057158c();
  *(undefined4 **)(unaff_EBP + -0x14) = extraout_ECX;
  FUN__text__005320fd(*(undefined4 *)(unaff_EBP + 8),0,1);
  uVar1 = extraout_ECX[0x40c];
  uVar2 = extraout_ECX[0x40e] + 1 & 0xfffffffe;
  iVar4 = uVar2 - (uVar1 & 0xfffffffe);
  extraout_ECX[0x41e] = uVar2;
  *(undefined4 *)(unaff_EBP + -4) = 0;
  *extraout_ECX = &PTR_DAT_005d0eb0;
  extraout_ECX[0x41c] = uVar1 & 0xfffffffe;
  extraout_ECX[0x41d] = 0;
  extraout_ECX[0x420] = 0;
  extraout_ECX[0x41f] = 0;
  extraout_ECX[0x421] = 0;
  extraout_ECX[0x422] = iVar4;
  extraout_ECX[0x423] = 0;
  extraout_ECX[0x424] = 1;
  pvVar3 = (void *)FUN__text__00428a40(iVar4 * 0x10);
  *(void **)(unaff_EBP + -0x10) = pvVar3;
  *(undefined1 *)(unaff_EBP + -4) = 1;
  if (pvVar3 == (void *)0x0) {
    iVar4 = 0;
  }
  else {
    _vector_constructor_iterator_(pvVar3,0x10,iVar4,(_func_void_ptr_void_ptr *)&LAB__text__0052702e)
    ;
    iVar4 = *(int *)(unaff_EBP + -0x10);
  }
  extraout_ECX[0x41b] = iVar4;
  if (iVar4 == 0) {
    extraout_ECX[0x424] = 0;
  }
  if (*(int *)(*(int *)(unaff_EBP + 8) + 4) == 0x59565955) {
    extraout_ECX[0x425] = 8;
    extraout_ECX[0x426] = 0;
  }
  else {
    extraout_ECX[0x425] = 0;
    extraout_ECX[0x426] = 8;
  }
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return extraout_ECX;
}

