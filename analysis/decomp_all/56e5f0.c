
undefined4 FUN__text__0056e5f0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  
  if ((param_1 == 0) &&
     (iVar2 = FUN__text__00573780(2,"fprintf.c",0x38,0,"str != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_2 == 0) &&
     (iVar2 = FUN__text__00573780(2,"fprintf.c",0x39,0,"format != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  FUN__text__00577270(param_1);
  uVar3 = FUN__text__005777d0(param_1);
  uVar4 = FUN__text__00575940(param_1,param_2,&stack0x0000000c);
  FUN__text__00577930(uVar3,param_1);
  FUN__text__005772e0(param_1);
  return uVar4;
}

