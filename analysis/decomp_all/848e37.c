
uint FUN__text1__00848e37(short *param_1,short param_2)

{
  while( true ) {
    if ((*param_1 == 0) || (*param_1 == param_2)) break;
    param_1 = param_1 + 1;
  }
  return (uint)param_1 & ~-(uint)(*param_1 != param_2);
}

