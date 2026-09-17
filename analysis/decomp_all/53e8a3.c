
int __fastcall FUN__text__0053e8a3(int *param_1)

{
  int iVar1;
  int *local_8;
  
  if (param_1[0x11a] != 0) {
    local_8 = param_1;
    iVar1 = (**(code **)(*(int *)param_1[2] + 0x8c))((int *)param_1[2]);
    if (iVar1 < 0) {
      return iVar1;
    }
    if (param_1[0x11b] == 0) {
      if (param_1[0x118] == 1) {
        iVar1 = (**(code **)(*(int *)param_1[0xd] + 0x3c))((int *)param_1[0xd],param_1[0x119]);
      }
      else {
        iVar1 = (**(code **)(*(int *)param_1[0xc] + 0x3c))((int *)param_1[0xc],0,&local_8);
      }
      if (iVar1 < 0) {
        return iVar1;
      }
      (**(code **)(*(int *)param_1[2] + 0x70))((int *)param_1[2],param_1[8],0,0,local_8,0);
      (**(code **)(*local_8 + 8))(local_8);
    }
    if (param_1[0x118] != 1) {
      if (1 < (uint)param_1[7]) {
        FUN__text__00529215(param_1[0xc],0,0,0xffffffff);
      }
      iVar1 = FUN__text__0053e316(param_1[0x119]);
      if (iVar1 < 0) {
        return iVar1;
      }
    }
    param_1[0x11a] = 0;
  }
  return 0;
}

