
void FUN__text__0052e391(void)

{
  int iVar1;
  
  iVar1 = FUN__text__00541c1c();
  if (iVar1 == 0) {
    PTR_DAT_0075e310 = FUN__text__0052dff0;
    PTR_DAT_0075e314 = FUN__text__0052e167;
  }
  else {
    PTR_DAT_0075e310 = FUN__text__0052e24f;
    PTR_DAT_0075e314 = FUN__text__0052e24f;
  }
                    /* WARNING: Could not recover jumptable at 0x0052e3c3. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_DAT_0075e310)();
  return;
}

