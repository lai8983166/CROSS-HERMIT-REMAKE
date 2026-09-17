
undefined4 FUN__text__00572990(char *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  char *local_24;
  size_t local_20;
  char *local_1c;
  undefined4 local_18;
  
  if ((param_1 == (char *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"sscanf.c",0x42,0,"string != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_2 == 0) &&
     (iVar2 = FUN__text__00573780(2,"sscanf.c",0x43,0,"format != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  local_18 = 0x49;
  local_1c = param_1;
  local_24 = param_1;
  local_20 = _strlen(param_1);
  uVar3 = FUN__text__0057f450(&local_24,param_2,&stack0x0000000c);
  return uVar3;
}

