
void __thiscall FUN__text__00406b70(int param_1,int *param_2,void *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_8 = param_1;
    for (local_10 = 0; local_10 != *(short *)(local_8 + 0x3e); local_10 = local_10 + 1) {
      local_14 = param_2[1] + local_10 * *param_2;
      _memset(param_3,0,(int)*(short *)(local_8 + 0x3c) << 1);
      for (local_c = 0; local_c != *param_2; local_c = local_c + 1) {
        if (local_c < *(short *)(local_8 + 0x38)) {
          if (*(char *)(local_14 + local_c) == '\0') {
            FUN__text__0056cda0(param_3,&DAT_005926c4);
          }
          else {
            FUN__text__0056cda0(param_3,&DAT_005926c8);
          }
        }
        else {
          FUN__text__0056cda0(param_3,&DAT_005926cc);
        }
      }
      FUN__text__0056cda0(param_3,&DAT_005926c0);
      (*API_KERNEL32_DLL_OutputDebugStringA)(param_3);
      FUN__text__0056ce80();
    }
  }
  local_8 = 0x406c95;
  FUN__text__0056ce80();
  return;
}

