
undefined4 FUN__text__0056e4a0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  if ((param_1 == 0) &&
     (iVar2 = FUN__text__00573780(2,"fclose.c",0x3a,0,"stream != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((*(uint *)(param_1 + 0xc) & 0x40) == 0) {
    FUN__text__00577270(param_1);
    local_8 = FUN__text__0056e530(param_1);
    FUN__text__005772e0(param_1);
  }
  else {
    *(undefined4 *)(param_1 + 0xc) = 0;
  }
  return local_8;
}

