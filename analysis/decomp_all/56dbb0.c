
undefined4 FUN__text__0056dbb0(undefined1 *param_1,int param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 *local_24;
  int local_20;
  undefined1 *local_1c;
  undefined4 local_18;
  
  if ((param_1 == (undefined1 *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"vsprintf.c",0x5a,0,"string != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_2 == 0) &&
     (iVar2 = FUN__text__00573780(2,"vsprintf.c",0x5b,0,"format != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  local_18 = 0x42;
  local_1c = param_1;
  local_24 = param_1;
  local_20 = 0x7fffffff;
  uVar3 = FUN__text__00575940(&local_24,param_2,param_3);
  local_20 = local_20 + -1;
  if (local_20 < 0) {
    FUN__text__005756c0(0,&local_24);
  }
  else {
    *local_24 = 0;
  }
  return uVar3;
}

