
int FUN__text__005873f0(int param_1,uint param_2,undefined4 param_3,int param_4,undefined4 param_5,
                       int param_6,int param_7,int param_8)

{
  int iVar1;
  int iVar2;
  int iStack_8c;
  uint uStack_88;
  undefined1 *puStack_84;
  int iStack_80;
  undefined4 uStack_7c;
  undefined4 uStack_78;
  int iStack_74;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  int iStack_68;
  undefined1 *puStack_64;
  int iStack_60;
  int iStack_5c;
  uint uStack_58;
  undefined *puStack_54;
  int iStack_50;
  undefined4 uStack_4c;
  int iStack_48;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fae28;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  ExceptionList = &local_14;
  if (DAT_0080a6b8 == 0) {
    iStack_48 = 0;
    uStack_4c = 0;
    iStack_50 = 1;
    puStack_54 = &DAT_005fae14;
    uStack_58 = 0x100;
    iStack_5c = 0;
    iStack_60 = 0x587437;
    ExceptionList = &local_14;
    iVar1 = (*API_KERNEL32_DLL_LCMapStringW)();
    if (iVar1 == 0) {
      iStack_48 = 0;
      uStack_4c = 0;
      iStack_50 = 1;
      puStack_54 = &DAT_005fae10;
      uStack_58 = 0x100;
      iStack_5c = 0;
      iStack_60 = 0x58745f;
      iVar1 = (*API_KERNEL32_DLL_LCMapStringA)();
      if (iVar1 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_0080a6b8 = 2;
    }
    else {
      DAT_0080a6b8 = 1;
    }
  }
  if (0 < param_4) {
    iStack_48 = param_4;
    uStack_4c = param_3;
    iStack_50 = 0x587489;
    param_4 = FUN__text__00587700();
  }
  if (DAT_0080a6b8 == 2) {
    iStack_48 = param_6;
    uStack_4c = param_5;
    iStack_50 = param_4;
    puStack_54 = (undefined *)param_3;
    uStack_58 = param_2;
    iStack_5c = param_1;
    iStack_60 = 0x5874b6;
    iVar1 = (*API_KERNEL32_DLL_LCMapStringA)();
  }
  else if (DAT_0080a6b8 == 1) {
    if (param_7 == 0) {
      param_7 = DAT_0080a63c;
    }
    iStack_48 = 0;
    uStack_4c = 0;
    iStack_50 = param_4;
    puStack_54 = (undefined *)param_3;
    uStack_58 = (-(uint)(param_8 != 0) & 8) + 1;
    iStack_5c = param_7;
    iStack_60 = 0x5874fb;
    iVar2 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
    if (iVar2 == 0) {
      iVar1 = 0;
    }
    else {
      local_8 = 0;
      iStack_60 = 0x587521;
      FUN__text__0056e230();
      local_8 = 0xffffffff;
      if (&stack0x00000000 == (undefined1 *)0x5c) {
        iVar1 = 0;
      }
      else {
        iStack_68 = param_4;
        uStack_6c = param_3;
        uStack_70 = 1;
        iStack_74 = param_7;
        uStack_78 = 0x587576;
        puStack_64 = (undefined1 *)&iStack_5c;
        iStack_60 = iVar2;
        iVar1 = (*API_KERNEL32_DLL_MultiByteToWideChar)();
        if (iVar1 == 0) {
          iVar1 = 0;
        }
        else {
          uStack_78 = 0;
          uStack_7c = 0;
          uStack_88 = param_2;
          iStack_8c = param_1;
          puStack_84 = (undefined1 *)&iStack_5c;
          iStack_80 = iVar2;
          iVar1 = (*API_KERNEL32_DLL_LCMapStringW)();
          if (iVar1 == 0) {
            iVar1 = 0;
          }
          else if ((param_2 & 0x400) == 0) {
            local_8 = 1;
            FUN__text__0056e230();
            local_8 = 0xffffffff;
            if (&stack0x00000000 == (undefined1 *)0x8c) {
              iVar1 = 0;
            }
            else {
              iVar2 = (*API_KERNEL32_DLL_LCMapStringW)
                                (param_1,param_2,&iStack_5c,iVar2,&iStack_8c,iVar1);
              if (iVar2 == 0) {
                iVar1 = 0;
              }
              else if (param_6 == 0) {
                iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                                  (param_7,0x220,&iStack_8c,iVar1,0,0,0,0);
                if (iVar1 == 0) {
                  iVar1 = 0;
                }
              }
              else {
                iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                                  (param_7,0x220,&iStack_8c,iVar1,param_5,param_6,0,0);
                if (iVar1 == 0) {
                  iVar1 = 0;
                }
              }
            }
          }
          else if (param_6 != 0) {
            if (param_6 < iVar1) {
              iVar1 = 0;
            }
            else {
              iVar2 = (*API_KERNEL32_DLL_LCMapStringW)
                                (param_1,param_2,&iStack_5c,iVar2,param_5,param_6);
              if (iVar2 == 0) {
                iVar1 = 0;
              }
            }
          }
        }
      }
    }
  }
  else {
    iVar1 = 0;
  }
  ExceptionList = local_14;
  return iVar1;
}

