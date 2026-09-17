
char * FUN__text1__00834345(uint *param_1,undefined4 *param_2,char param_3)

{
  uint *puVar1;
  undefined4 uVar2;
  void *pvVar3;
  DWORD DVar4;
  int iVar5;
  undefined4 *puVar6;
  CHAR local_110;
  undefined4 local_10f;
  int local_10;
  void *local_c;
  char local_8;
  
  *param_2 = 0;
  local_8 = *(char *)param_1;
  puVar1 = (uint *)((int)param_1 + 1);
  if (local_8 == '\x01') {
    if (param_3 == '\0') {
      uVar2 = FUN__text1__00835a40(0);
      *param_2 = uVar2;
    }
  }
  else if ((local_8 == '\x02') || (local_8 == '\x03')) {
    DAT_008751fc = (uint)(ushort)*puVar1;
    iVar5 = *(int *)((int)param_1 + 3);
    param_1 = (uint *)((int)param_1 + 7);
    pvVar3 = operator_new(iVar5 + 0x10000);
    local_c = pvVar3;
    while( true ) {
      local_10 = iVar5 + 0x10000;
      param_1 = (uint *)FUN__text1__00834599(param_1,local_c,&local_10,0);
      if (param_1 == (uint *)0x0) {
        return (char *)0x0;
      }
      if (local_10 == 0) break;
      local_c = (void *)((int)local_c + local_10);
    }
    local_110 = DAT_00874e88;
    puVar6 = &local_10f;
    for (iVar5 = 0x3f; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar6 = 0;
      puVar6 = puVar6 + 1;
    }
    *(undefined2 *)puVar6 = 0;
    *(undefined1 *)((int)puVar6 + 2) = 0;
    DVar4 = GetEnvironmentVariableA("ARMSPLASHOFF",&local_110,0x100);
    if (DVar4 == 0) {
      local_110 = '\0';
    }
    else if ((local_110 == '0') || (local_110 == '\0')) {
      local_110 = '\0';
    }
    else {
      local_110 = '\x01';
    }
    if ((((local_110 == '\0') && (param_3 == '\0')) && (DAT_008751ec != 8)) && (DAT_008751ec != 9))
    {
      FUN__text1__00836597(pvVar3,local_8 == '\x03',0);
    }
    FUN__text1__00848476(pvVar3);
    puVar1 = param_1;
  }
  while (param_1 = puVar1, (char)*param_1 != '\0') {
    param_1 = (uint *)((int)param_1 + 5);
    while( true ) {
      puVar1 = param_1 + 1;
      if ((*param_1 & 0x7fffffff) == 0) break;
      param_1 = (uint *)((int)(param_1 + 1) + (*param_1 & 0x7fffffff));
    }
  }
  return (char *)((int)param_1 + 1);
}

