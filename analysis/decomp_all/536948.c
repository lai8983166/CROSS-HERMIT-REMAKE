
void FUN__text__00536948(void)

{
  undefined4 *extraout_ECX;
  int unaff_EBP;
  
  FUN__text__0057158c();
  *(undefined4 **)(unaff_EBP + -0x10) = extraout_ECX;
  *extraout_ECX = &PTR_DAT_005d0eb0;
  *(undefined4 *)(unaff_EBP + -4) = 0;
  FUN__text__00535667();
  if (extraout_ECX[0x41b] != 0) {
    FUN__text__00428ad0(extraout_ECX[0x41b]);
  }
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  FUN__text__0053184f();
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return;
}

