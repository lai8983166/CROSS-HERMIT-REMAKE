
bool FUN__text1__00833f70(char *param_1)

{
  char cVar1;
  int iVar2;
  
  iVar2 = 10;
  do {
    if (iVar2 == 0) break;
    iVar2 = iVar2 + -1;
    cVar1 = *param_1;
    param_1 = param_1 + 1;
  } while (cVar1 != -0x34);
  return iVar2 != 0;
}

