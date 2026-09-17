
void FUN__text1__0083d9e7(undefined4 param_1)

{
  int iVar1;
  
  iVar1 = FUN__text1__0083d81c(param_1,1);
  if (-1 < iVar1) {
    FUN__text1__00848476(*(undefined4 *)(DAT_008752c0 + iVar1 * 4));
    DAT_0087542c = DAT_0087542c + -1;
    FUN__text1__008487d0
              (DAT_008752c0 + iVar1 * 4,DAT_008752c0 + 4 + iVar1 * 4,(DAT_0087542c - iVar1) * 4);
  }
  return;
}

