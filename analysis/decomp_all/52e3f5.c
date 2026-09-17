
void FUN__text__0052e3f5(void)

{
  int iVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  iVar1 = FUN__text__00541c1c();
  if (iVar1 == 0) {
    PTR_DAT_0075e310 = FUN__text__0052dff0;
    UNRECOVERED_JUMPTABLE = FUN__text__0052e167;
  }
  else {
    UNRECOVERED_JUMPTABLE = FUN__text__0052e24f;
    PTR_DAT_0075e310 = FUN__text__0052e24f;
  }
  PTR_DAT_0075e314 = UNRECOVERED_JUMPTABLE;
                    /* WARNING: Could not recover jumptable at 0x0052e422. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)();
  return;
}

