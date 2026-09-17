
undefined4 FUN__text__0056e6c0(char *param_1,char *param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  
  if ((param_1 == (char *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"fopen.c",0x35,0,"file != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((*param_1 == '\0') &&
     (iVar2 = FUN__text__00573780(2,"fopen.c",0x36,0,"*file != _T(\'\\0\')"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_2 == (char *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"fopen.c",0x37,0,"mode != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((*param_2 == '\0') &&
     (iVar2 = FUN__text__00573780(2,"fopen.c",0x38,0,"*mode != _T(\'\\0\')"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  iVar2 = FUN__text__00577d60();
  if (iVar2 == 0) {
    uVar3 = 0;
  }
  else {
    uVar3 = FUN__text__005779d0(param_1,param_2,param_3,iVar2);
    FUN__text__005772e0(iVar2);
  }
  return uVar3;
}

