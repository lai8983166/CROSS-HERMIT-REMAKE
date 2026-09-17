
void FUN__text__00545400(int param_1,int param_2)

{
  char *pcVar1;
  char cVar2;
  char cVar3;
  int iStack_c;
  
  if (param_2 != 0) {
    if (param_1 == 1) {
      iStack_c = 2;
      cVar3 = -1;
    }
    else if (param_1 == 2) {
      iStack_c = 4;
      cVar3 = 'U';
    }
    else if (param_1 == 4) {
      iStack_c = 0x10;
      cVar3 = '\x11';
    }
    else if (param_1 == 8) {
      iStack_c = 0x100;
      cVar3 = '\x01';
    }
    else {
      iStack_c = 0;
      cVar3 = '\0';
    }
    cVar2 = '\0';
    if (iStack_c != 0) {
      pcVar1 = (char *)(param_2 + 2);
      do {
        pcVar1[-2] = cVar2;
        pcVar1[-1] = cVar2;
        *pcVar1 = cVar2;
        pcVar1 = pcVar1 + 3;
        cVar2 = cVar2 + cVar3;
        iStack_c = iStack_c + -1;
      } while (iStack_c != 0);
    }
  }
  return;
}

