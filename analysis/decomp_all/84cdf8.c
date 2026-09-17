
int FUN__text1__0084cdf8(int param_1)

{
  int iVar1;
  bool bVar2;
  
  if (param_1 == -2) {
    DAT_008758a4 = 1;
                    /* WARNING: Could not recover jumptable at 0x0084ce12. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetOEMCP();
    return iVar1;
  }
  if (param_1 == -3) {
    DAT_008758a4 = 1;
                    /* WARNING: Could not recover jumptable at 0x0084ce27. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetACP();
    return iVar1;
  }
  bVar2 = param_1 == -4;
  if (bVar2) {
    param_1 = DAT_008758cc;
  }
  DAT_008758a4 = (uint)bVar2;
  return param_1;
}

