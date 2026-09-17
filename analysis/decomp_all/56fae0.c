
undefined4 FUN_0056fae0(char *param_1,char param_2,int param_3)

{
  code *pcVar1;
  char *pcVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 local_8;
  
  local_8 = 1;
  pcVar2 = param_1;
  while( true ) {
    do {
      param_1 = pcVar2;
      iVar4 = param_3 + -1;
      if (param_3 == 0) {
        return local_8;
      }
      pcVar2 = param_1 + 1;
      param_3 = iVar4;
    } while (*param_1 == param_2);
    iVar4 = FUN_00573780(0,0,0,0,"memory check error at 0x%08X = 0x%02X, should be 0x%02X.\n",
                         param_1,*param_1,param_2);
    if (iVar4 == 1) break;
    local_8 = 0;
  }
  pcVar1 = (code *)swi(3);
  uVar3 = (*pcVar1)();
  return uVar3;
}

