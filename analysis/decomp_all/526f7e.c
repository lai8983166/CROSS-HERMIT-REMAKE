
int FUN__text__00526f7e(void)

{
  int unaff_EBP;
  int iVar1;
  
  FUN__text__0057158c();
  FUN__text__0052b0a9();
  *(undefined4 *)(unaff_EBP + -4) = 0;
  FUN__text__00531042();
  *(undefined1 *)(unaff_EBP + -4) = 1;
  if ((*(int *)(unaff_EBP + 8) == 0) || (*(int *)(unaff_EBP + 0x10) == 0)) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar1 = FUN__text__005310dc(unaff_EBP + -0xbc,*(undefined4 *)(unaff_EBP + 0x10),
                                *(undefined4 *)(unaff_EBP + 0x14),*(undefined4 *)(unaff_EBP + 0x18),
                                0,1);
    if (((-1 < iVar1) && (iVar1 = FUN__text__0052b137(unaff_EBP + -0xbc), -1 < iVar1)) &&
       (iVar1 = FUN__text__0052d1c2(*(undefined4 *)(unaff_EBP + 8),*(undefined4 *)(unaff_EBP + 0xc),
                                    *(undefined4 *)(unaff_EBP + 0x1c)), -1 < iVar1)) {
      iVar1 = 0;
    }
  }
  *(undefined1 *)(unaff_EBP + -4) = 0;
  thunk_FUN__text__00531052();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  FUN__text__0052b0c2();
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return iVar1;
}

