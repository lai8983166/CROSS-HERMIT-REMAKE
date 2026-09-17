
int FUN__text__00548d89(int param_1,int *param_2)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = DAT_0080a398;
  while( true ) {
    if (piVar1 == (int *)0x0) {
      iVar2 = FUN__text__00428a40(0xb0);
      if (iVar2 == 0) {
        iVar2 = 0;
      }
      else {
        iVar2 = FUN__text__005483b1();
      }
      if (iVar2 == 0) {
        iVar3 = -0x7ff8fff2;
      }
      else {
        iVar3 = FUN__text__00548735(param_1);
        if (iVar3 < 0) {
          FUN__text__005484f8(1);
        }
        else {
          *param_2 = iVar2;
          iVar3 = 0;
        }
      }
      return iVar3;
    }
    if (piVar1[1] == param_1) break;
    piVar1 = (int *)piVar1[0x2b];
  }
  *piVar1 = *piVar1 + 1;
  *param_2 = (int)piVar1;
  return 0;
}

