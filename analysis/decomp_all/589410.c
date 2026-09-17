
undefined4 FUN__text__00589410(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  
  if ((param_2 == 0) &&
     (iVar2 = FUN__text__00573780(2,"ungetc.c",0x31,0,"stream != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  FUN__text__00577270(param_2);
  uVar3 = FUN__text__00589480(param_1,param_2);
  FUN__text__005772e0(param_2);
  return uVar3;
}

