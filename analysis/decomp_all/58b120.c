
undefined2 FUN__text__0058b120(undefined2 param_1,int param_2)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  undefined2 extraout_var;
  
  if ((param_2 == 0) && (iVar3 = FUN__text__00573780(2,"fputwc.c",0x35,0,"str != NULL"), iVar3 == 1)
     ) {
    pcVar1 = (code *)swi(3);
    uVar2 = (*pcVar1)();
    return uVar2;
  }
  FUN__text__00577270(param_2);
  uVar2 = FUN__text__0058b1a0(CONCAT22(extraout_var,param_1),param_2);
  FUN__text__005772e0(param_2);
  return uVar2;
}

