
undefined4
FUN__text__0058acd0(undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,int param_5
                   ,int param_6)

{
  undefined1 *puVar1;
  int iVar2;
  undefined4 uVar3;
  size_t _Size;
  int aiStack_84 [3];
  int iStack_78;
  undefined1 *puStack_74;
  int aiStack_64 [5];
  undefined *puStack_50;
  int iStack_4c;
  undefined1 *puStack_48;
  undefined1 local_20 [4];
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fb010;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  local_1c = &stack0xffffffbc;
  ExceptionList = &local_14;
  puVar1 = &stack0xffffffbc;
  if (DAT_0080a788 == 0) {
    puStack_48 = local_20;
    iStack_4c = 1;
    puStack_50 = &DAT_005fae14;
    aiStack_64[4] = 1;
    aiStack_64[3] = 0x58ad12;
    ExceptionList = &local_14;
    iVar2 = (*API_KERNEL32_DLL_GetStringTypeW)();
    if (iVar2 == 0) {
      puStack_48 = local_20;
      iStack_4c = 1;
      puStack_50 = &DAT_005fae10;
      aiStack_64[4] = 1;
      aiStack_64[3] = 0;
      aiStack_64[2] = 0x58ad37;
      iVar2 = (*API_KERNEL32_DLL_GetStringTypeExA)();
      if (iVar2 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_0080a788 = 2;
      puVar1 = local_1c;
    }
    else {
      DAT_0080a788 = 1;
      puVar1 = local_1c;
    }
  }
  local_1c = puVar1;
  if (DAT_0080a788 == 1) {
    puStack_48 = (undefined1 *)param_4;
    iStack_4c = param_3;
    puStack_50 = (undefined *)param_2;
    aiStack_64[4] = param_1;
    aiStack_64[3] = 0x58ad6d;
    uVar3 = (*API_KERNEL32_DLL_GetStringTypeW)();
  }
  else if (DAT_0080a788 == 2) {
    if (param_5 == 0) {
      param_5 = DAT_0080a63c;
    }
    puStack_48 = (undefined1 *)0x0;
    iStack_4c = 0;
    puStack_50 = (undefined *)0x0;
    aiStack_64[4] = 0;
    aiStack_64[3] = param_3;
    aiStack_64[2] = param_2;
    aiStack_64[1] = 0x220;
    aiStack_64[0] = param_5;
    _Size = (*API_KERNEL32_DLL_WideCharToMultiByte)();
    if (_Size == 0) {
      uVar3 = 0;
    }
    else {
      local_8 = 0;
      FUN__text__0056e230();
      puStack_74 = (undefined1 *)0x58adeb;
      local_1c = (undefined1 *)aiStack_64;
      _memset(aiStack_64,0,_Size);
      local_8 = 0xffffffff;
      if (&stack0x00000000 == (undefined1 *)0x64) {
        uVar3 = 0;
      }
      else {
        iStack_78 = param_3;
        aiStack_84[2] = param_2;
        aiStack_84[1] = 0x220;
        aiStack_84[0] = param_5;
        puStack_74 = (undefined1 *)aiStack_64;
        iVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)();
        if (iVar2 == 0) {
          uVar3 = 0;
        }
        else {
          local_8 = 1;
          FUN__text__0056e230();
          local_8 = 0xffffffff;
          if (&stack0x00000000 == (undefined1 *)0x84) {
            uVar3 = 0;
          }
          else {
            if (param_6 == 0) {
              param_6 = DAT_0080a62c;
            }
            *(undefined2 *)((int)aiStack_84 + param_3 * 2) = 0xffff;
            *(undefined2 *)(&stack0xffffff7a + param_3 * 2) = 0xffff;
            local_1c = (undefined1 *)aiStack_84;
            uVar3 = (*API_KERNEL32_DLL_GetStringTypeExA)
                              (param_6,param_1,aiStack_64,_Size,aiStack_84);
            if ((*(short *)(&stack0xffffff7a + param_3 * 2) == -1) ||
               (*(short *)((int)aiStack_84 + param_3 * 2) != -1)) {
              uVar3 = 0;
            }
            else {
              FUN__text__005855a0(param_4,aiStack_84,param_3 << 1);
            }
          }
        }
      }
    }
  }
  else {
    uVar3 = 0;
  }
  ExceptionList = local_14;
  return uVar3;
}

