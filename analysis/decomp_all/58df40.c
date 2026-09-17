
undefined4
FUN__text__0058df40(int param_1,undefined4 param_2,byte *param_3,int param_4,byte *param_5,
                   int param_6,int param_7)

{
  code *pcVar1;
  undefined1 *puVar2;
  int iVar3;
  undefined4 uVar4;
  int aiStack_a0 [2];
  byte *pbStack_98;
  int iStack_94;
  undefined4 uStack_90;
  undefined4 uStack_8c;
  int iStack_88;
  undefined4 uStack_84;
  byte *pbStack_80;
  int iStack_7c;
  undefined1 *puStack_78;
  int iStack_74;
  int iStack_70;
  undefined4 uStack_6c;
  byte *pbStack_68;
  int iStack_64;
  byte *pbStack_60;
  uint *puStack_5c;
  byte *local_44;
  uint local_40;
  byte local_3a [14];
  undefined1 *local_2c;
  undefined1 *local_28;
  int local_24;
  int local_20;
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fb0e0;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  local_1c = &stack0xffffffa8;
  ExceptionList = &local_14;
  puVar2 = &stack0xffffffa8;
  if (DAT_0080a798 == 0) {
    puStack_5c = (uint *)0x1;
    pbStack_60 = &DAT_005fae14;
    iStack_64 = 1;
    pbStack_68 = &DAT_005fae14;
    uStack_6c = 0;
    iStack_70 = 0;
    iStack_74 = 0x58df87;
    ExceptionList = &local_14;
    iVar3 = (*API_KERNEL32_DLL_CompareStringW)();
    if (iVar3 == 0) {
      puStack_5c = (uint *)0x1;
      pbStack_60 = &DAT_005fae10;
      iStack_64 = 1;
      pbStack_68 = &DAT_005fae10;
      uStack_6c = 0;
      iStack_70 = 0;
      iStack_74 = 0x58dfaf;
      iVar3 = (*API_KERNEL32_DLL_CompareStringA)();
      if (iVar3 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_0080a798 = 2;
      puVar2 = local_1c;
    }
    else {
      DAT_0080a798 = 1;
      puVar2 = local_1c;
    }
  }
  local_1c = puVar2;
  if (0 < param_4) {
    puStack_5c = (uint *)param_4;
    pbStack_60 = param_3;
    iStack_64 = 0x58dfd9;
    param_4 = FUN__text__0058e340();
  }
  if (0 < param_6) {
    puStack_5c = (uint *)param_6;
    pbStack_60 = param_5;
    iStack_64 = 0x58dff2;
    param_6 = FUN__text__0058e340();
  }
  if (DAT_0080a798 == 2) {
    puStack_5c = (uint *)param_6;
    pbStack_60 = param_5;
    iStack_64 = param_4;
    pbStack_68 = param_3;
    uStack_6c = param_2;
    iStack_70 = param_1;
    iStack_74 = 0x58e01f;
    uVar4 = (*API_KERNEL32_DLL_CompareStringA)();
  }
  else if (DAT_0080a798 == 1) {
    if (param_7 == 0) {
      param_7 = DAT_0080a63c;
    }
    if ((param_4 == 0) || (param_6 == 0)) {
      if (param_4 == param_6) {
        ExceptionList = local_14;
        return 2;
      }
      if (1 < param_6) {
        ExceptionList = local_14;
        return 1;
      }
      if (1 < param_4) {
        ExceptionList = local_14;
        return 3;
      }
      puStack_5c = &local_40;
      pbStack_60 = (byte *)param_7;
      iStack_64 = 0x58e090;
      iVar3 = (*API_KERNEL32_DLL_GetCPInfo)();
      if (iVar3 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      if (((param_4 != 0) || (param_6 != 1)) && ((param_4 != 1 || (param_6 != 0)))) {
        puStack_5c = (uint *)0x5fb0a0;
        pbStack_60 = (byte *)0x0;
        iStack_64 = 0xb6;
        pbStack_68 = (byte *)0x5fb098;
        uStack_6c = 2;
        iStack_70 = 0x58e0cb;
        iVar3 = FUN__text__00573780();
        if (iVar3 == 1) {
          pcVar1 = (code *)swi(3);
          uVar4 = (*pcVar1)();
          return uVar4;
        }
      }
      if (0 < param_4) {
        if (local_40 < 2) {
          ExceptionList = local_14;
          return 3;
        }
        local_44 = local_3a;
        while( true ) {
          if ((*local_44 == 0) || (local_44[1] == 0)) {
            ExceptionList = local_14;
            return 3;
          }
          if ((*local_44 <= *param_3) && (*param_3 <= local_44[1])) break;
          local_44 = local_44 + 2;
        }
        ExceptionList = local_14;
        return 2;
      }
      if (0 < param_6) {
        if (local_40 < 2) {
          ExceptionList = local_14;
          return 1;
        }
        local_44 = local_3a;
        while( true ) {
          if ((*local_44 == 0) || (local_44[1] == 0)) {
            ExceptionList = local_14;
            return 1;
          }
          if ((*local_44 <= *param_5) && (*param_5 <= local_44[1])) break;
          local_44 = local_44 + 2;
        }
        ExceptionList = local_14;
        return 2;
      }
    }
    puStack_5c = (uint *)0x0;
    pbStack_60 = (byte *)0x0;
    iStack_64 = param_4;
    pbStack_68 = param_3;
    uStack_6c = 9;
    iStack_70 = param_7;
    iStack_74 = 0x58e1e4;
    local_20 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
    if (local_20 == 0) {
      uVar4 = 0;
    }
    else {
      local_8 = 0;
      iStack_74 = 0x58e20a;
      FUN__text__0056e230();
      local_8 = 0xffffffff;
      if (&stack0x00000000 == (undefined1 *)0x70) {
        uVar4 = 0;
      }
      else {
        iStack_74 = local_20;
        iStack_7c = param_4;
        pbStack_80 = param_3;
        uStack_84 = 1;
        iStack_88 = param_7;
        uStack_8c = 0x58e25f;
        puStack_78 = (undefined1 *)&iStack_70;
        local_28 = (undefined1 *)&iStack_70;
        local_1c = (undefined1 *)&iStack_70;
        iVar3 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
        if (iVar3 == 0) {
          uVar4 = 0;
        }
        else {
          uStack_8c = 0;
          uStack_90 = 0;
          iStack_94 = param_6;
          pbStack_98 = param_5;
          aiStack_a0[1] = 9;
          aiStack_a0[0] = param_7;
          local_24 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
          if (local_24 == 0) {
            uVar4 = 0;
          }
          else {
            local_8 = 1;
            FUN__text__0056e230();
            local_8 = 0xffffffff;
            if (&stack0x00000000 == (undefined1 *)0xa0) {
              uVar4 = 0;
            }
            else {
              local_2c = (undefined1 *)aiStack_a0;
              local_1c = (undefined1 *)aiStack_a0;
              iVar3 = (*API_KERNEL32_DLL_MultiByteToWideChar)
                                (param_7,1,param_5,param_6,aiStack_a0,local_24);
              if (iVar3 == 0) {
                uVar4 = 0;
              }
              else {
                uVar4 = (*API_KERNEL32_DLL_CompareStringW)
                                  (param_1,param_2,local_28,local_20,local_2c,local_24);
              }
            }
          }
        }
      }
    }
  }
  else {
    uVar4 = 0;
  }
  ExceptionList = local_14;
  return uVar4;
}

