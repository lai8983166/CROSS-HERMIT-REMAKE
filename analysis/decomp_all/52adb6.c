
int FUN__text__0052adb6(undefined4 param_1,int param_2,int param_3)

{
  char cVar1;
  int iVar2;
  char *pcVar3;
  
  pcVar3 = &stack0xfffffff4;
  if ((param_2 != 0) && (param_3 != 0)) {
    FUN__text__0056e230();
    iVar2 = FUN__text__0052ab47(param_1,&stack0xfffffff4,param_3);
    if (iVar2 < 0) {
      return iVar2;
    }
    do {
      cVar1 = *pcVar3;
      pcVar3 = pcVar3 + 1;
    } while (cVar1 != '\0');
    (*API_KERNEL32_DLL_MultiByteToWideChar)
              (0,0,&stack0xfffffff4,(int)pcVar3 - (int)&stack0xfffffff5,param_2,param_3);
  }
  return 0;
}

