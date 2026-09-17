
uint FUN__text1__00848e85(short *param_1,short param_2)

{
  short *psVar1;
  short sVar2;
  
  sVar2 = *param_1;
  psVar1 = param_1;
  while (sVar2 != 0) {
    sVar2 = psVar1[1];
    psVar1 = psVar1 + 1;
  }
  for (; (psVar1 != param_1 && (*psVar1 != param_2)); psVar1 = psVar1 + -1) {
  }
  return (uint)psVar1 & ~-(uint)(*psVar1 != param_2);
}

