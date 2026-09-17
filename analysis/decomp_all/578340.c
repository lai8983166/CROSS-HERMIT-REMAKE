
void FUN__text__00578340(int param_1,uint param_2)

{
  int iVar1;
  uint local_4c;
  uint local_48;
  uint local_44;
  uint local_40;
  undefined4 local_3c;
  uint local_38;
  byte *local_34;
  undefined4 local_30;
  int local_2c;
  int local_28;
  uint local_24;
  uint local_20;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa280;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  local_20 = param_2;
  if (param_1 == 0) {
    ExceptionList = &pvStack_14;
    __malloc_base(param_2);
    FUN__text__005787c2();
    return;
  }
  if (param_2 == 0) {
    ExceptionList = &pvStack_14;
    FUN__text__005787e0(param_1);
    FUN__text__005787c2();
    return;
  }
  ExceptionList = &pvStack_14;
  if (DAT_0080ab2c != 3) {
    ExceptionList = &pvStack_14;
    if (DAT_0080ab2c != 2) {
      while( true ) {
        local_28 = 0;
        if (param_2 < 0xffffffe1) {
          if (param_2 == 0) {
            param_2 = 1;
          }
          param_2 = param_2 + 0xf & 0xfffffff0;
          local_28 = (*API_NTDLL_DLL_RtlReAllocateHeap)(DAT_0080ab28,0,param_1,param_2);
        }
        if ((local_28 != 0) || (DAT_0080a4ec == 0)) break;
        iVar1 = __callnewh(param_2);
        if (iVar1 == 0) {
          FUN__text__005787c2();
          return;
        }
      }
      FUN__text__005787c2();
      return;
    }
    ExceptionList = &pvStack_14;
    if (param_2 < 0xffffffe1) {
      if (param_2 == 0) {
        param_2 = 0x10;
        ExceptionList = &pvStack_14;
      }
      else {
        param_2 = param_2 + 0xf & 0xfffffff0;
        ExceptionList = &pvStack_14;
      }
    }
    while( true ) {
      local_28 = 0;
      if (param_2 < 0xffffffe1) {
        FUN__text__00577040(9);
        local_8 = 1;
        local_34 = (byte *)FUN__text__0057ac20(param_1,&local_3c,&local_30);
        if (local_34 == (byte *)0x0) {
          local_28 = (*API_NTDLL_DLL_RtlReAllocateHeap)(DAT_0080ab28,0,param_1,param_2);
        }
        else {
          if (param_2 < DAT_0076415c) {
            iVar1 = FUN__text__0057b390(local_3c,local_30,local_34,param_2 >> 4);
            if (iVar1 == 0) {
              local_28 = FUN__text__0057ad20(param_2 >> 4);
              if (local_28 != 0) {
                local_38 = (uint)*local_34 << 4;
                local_48 = local_38;
                if (param_2 <= local_38) {
                  local_48 = param_2;
                }
                FUN__text__0056d4d0(local_28,param_1,local_48);
                FUN__text__0057acb0(local_3c,local_30,local_34);
              }
            }
            else {
              local_28 = param_1;
            }
          }
          if ((local_28 == 0) &&
             (local_28 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,param_2), local_28 != 0)) {
            local_38 = (uint)*local_34 << 4;
            local_4c = local_38;
            if (param_2 <= local_38) {
              local_4c = param_2;
            }
            FUN__text__0056d4d0(local_28,param_1,local_4c);
            FUN__text__0057acb0(local_3c,local_30,local_34);
          }
        }
        local_8 = 0xffffffff;
        FUN__text__0057871f();
        FUN__text__0057872a();
        return;
      }
      if (DAT_0080a4ec == 0) break;
      iVar1 = __callnewh(param_2);
      if (iVar1 == 0) {
        FUN__text__005787c2();
        return;
      }
    }
    FUN__text__005787c2();
    return;
  }
  while( true ) {
    local_28 = 0;
    if (param_2 < 0xffffffe1) {
      FUN__text__00577040(9);
      local_8 = 0;
      local_2c = FUN__text__00578c00(param_1);
      if (local_2c != 0) {
        if (param_2 <= DAT_0080ab4c) {
          iVar1 = FUN__text__00579ae0(local_2c,param_1,param_2);
          if (iVar1 == 0) {
            local_28 = FUN__text__005792a0(param_2);
            if (local_28 != 0) {
              local_24 = *(int *)(param_1 + -4) - 1;
              local_40 = local_24;
              if (param_2 <= local_24) {
                local_40 = param_2;
              }
              FUN__text__0056d4d0(local_28,param_1,local_40);
              local_2c = FUN__text__00578c00(param_1);
              FUN__text__00578cc0(local_2c,param_1);
            }
          }
          else {
            local_28 = param_1;
          }
        }
        if (local_28 == 0) {
          if (param_2 == 0) {
            param_2 = 1;
          }
          local_44 = param_2 + 0xf & 0xfffffff0;
          local_28 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,local_44);
          if (local_28 != 0) {
            local_24 = *(int *)(param_1 + -4) - 1;
            if (local_24 < local_44) {
              local_44 = local_24;
            }
            FUN__text__0056d4d0(local_28,param_1,local_44);
            FUN__text__00578cc0(local_2c,param_1);
          }
        }
      }
      local_8 = 0xffffffff;
      FUN__text__00578508();
      FUN__text__00578513();
      return;
    }
    if (DAT_0080a4ec == 0) break;
    iVar1 = __callnewh(param_2);
    if (iVar1 == 0) {
      FUN__text__005787c2();
      return;
    }
  }
  FUN__text__005787c2();
  return;
}

