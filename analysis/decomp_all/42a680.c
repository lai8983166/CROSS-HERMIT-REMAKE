
void FUN__text__0042a680(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4,
                        int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_9c [16];
  int local_5c;
  int local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_48;
  undefined *local_38;
  undefined4 local_34;
  undefined4 local_20;
  undefined4 local_18;
  undefined4 uStack_c;
  undefined *local_8;
  
  puVar2 = local_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = (undefined *)0x0;
  _memset(&local_54,0,0x4c);
  _memset(&DAT_007a0fc0,0,0xf3c);
  if (param_2 != 0) {
    (*API_KERNEL32_DLL_lstrcpyA)(&DAT_007a0fc0,param_2);
    FUN__text__0056ce80();
  }
  local_54 = 0x4c;
  local_50 = param_1;
  local_48 = FUN__text__0042a5a0(param_4);
  local_38 = &DAT_007a0fc0;
  local_34 = 0xf3c;
  local_5c = param_5;
  if (param_5 == 0) {
    local_20 = 0x1004;
  }
  else if (param_5 == 1) {
    local_20 = 0x2006;
  }
  else if (param_5 == 2) {
    local_20 = 0x2004;
  }
  local_18 = FUN__text__0042a610(param_4);
  local_58 = FUN__text__00525ab2(&local_54);
  if (local_58 != 0) {
    local_8 = &DAT_007a0fc0;
  }
  uStack_c = 0x42a77f;
  FUN__text__0056ce80();
  return;
}

