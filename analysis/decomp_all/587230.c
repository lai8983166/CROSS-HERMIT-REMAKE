
undefined4
FUN_00587230(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,int param_5
            ,int param_6,int param_7)

{
  undefined1 *puVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *unaff_FS_OFFSET;
  int iStack_54;
  int iStack_50;
  undefined4 uStack_4c;
  undefined *puStack_48;
  undefined4 uStack_44;
  undefined1 *puStack_40;
  undefined1 local_20 [4];
  undefined1 *local_1c;
  undefined4 local_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fae18;
  puStack_10 = &DAT_00576b9c;
  local_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_14;
  local_1c = &stack0xffffffc4;
  puVar1 = &stack0xffffffc4;
  if (DAT_0080a6b4 == 0) {
    puStack_40 = local_20;
    uStack_44 = 1;
    puStack_48 = &DAT_005fae14;
    uStack_4c = 1;
    iStack_50 = 0x587272;
    iVar2 = (*API_KERNEL32_DLL_GetStringTypeW)();
    if (iVar2 == 0) {
      puStack_40 = local_20;
      uStack_44 = 1;
      puStack_48 = &DAT_005fae10;
      uStack_4c = 1;
      iStack_50 = 0;
      iStack_54 = 0x587297;
      iVar2 = (*API_KERNEL32_DLL_GetStringTypeExA)();
      if (iVar2 == 0) {
        uVar3 = 0;
        goto LAB_005873d8;
      }
      DAT_0080a6b4 = 2;
      puVar1 = local_1c;
    }
    else {
      DAT_0080a6b4 = 1;
      puVar1 = local_1c;
    }
  }
  local_1c = puVar1;
  if (DAT_0080a6b4 == 2) {
    if (param_6 == 0) {
      param_6 = DAT_0080a62c;
    }
    puStack_40 = (undefined1 *)param_4;
    uStack_44 = param_3;
    puStack_48 = (undefined *)param_2;
    uStack_4c = param_1;
    iStack_50 = param_6;
    iStack_54 = 0x5872e0;
    uVar3 = (*API_KERNEL32_DLL_GetStringTypeExA)();
  }
  else if (DAT_0080a6b4 == 1) {
    if (param_5 == 0) {
      param_5 = DAT_0080a63c;
    }
    puStack_40 = (undefined1 *)0x0;
    uStack_44 = 0;
    puStack_48 = (undefined *)param_3;
    uStack_4c = param_2;
    iStack_50 = (-(uint)(param_7 != 0) & 8) + 1;
    iStack_54 = param_5;
    iVar2 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
    if (iVar2 == 0) {
      uVar3 = 0;
    }
    else {
      local_8 = 0;
      FUN_0056e230();
      local_1c = (undefined1 *)&iStack_54;
      _memset(&iStack_54,0,iVar2 << 1);
      local_8 = 0xffffffff;
      if (&stack0x00000000 == (undefined1 *)0x54) {
        uVar3 = 0;
      }
      else {
        iVar2 = (*API_KERNEL32_DLL_MultiByteToWideChar)(param_5,1,param_2,param_3,&iStack_54,iVar2);
        if (iVar2 == 0) {
          uVar3 = 0;
        }
        else {
          uVar3 = (*API_KERNEL32_DLL_GetStringTypeW)(param_1,&iStack_54,iVar2,param_4);
        }
      }
    }
  }
  else {
    uVar3 = 0;
  }
LAB_005873d8:
  *unaff_FS_OFFSET = local_14;
  return uVar3;
}

