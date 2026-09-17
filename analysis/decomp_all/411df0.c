
void __fastcall FUN__text__00411df0(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && (param_1[2] != 0)) {
    local_8 = param_1;
    _memset(param_1 + 0x43,0,0x14);
    (**(code **)(*(int *)local_8[2] + 0x24))(local_8[2],0x14,local_8 + 0x43);
    local_c = FUN__text__0056ce80();
    if (local_c < 0) {
      local_1c = local_c;
      if ((local_c == -0x7ff8fff4) || (local_c == -0x7ff8ffe2)) {
        local_10 = 0;
        while( true ) {
          (**(code **)(*(int *)local_8[2] + 0x1c))(local_8[2]);
          local_20 = FUN__text__0056ce80();
          local_c = local_20;
          if ((local_20 != -0x7ff8ffe2) || (local_10 = local_10 + 1, 10000 < local_10)) break;
          local_20 = -0x7ff8ffe2;
          local_c = -0x7ff8ffe2;
        }
      }
      if (local_c < 0) {
        _memset(local_8 + 0x43,0,0x14);
      }
      else {
        (**(code **)(*(int *)local_8[2] + 0x24))(local_8[2],0x14,local_8 + 0x43);
        local_c = FUN__text__0056ce80();
      }
    }
    (*API_USER32_DLL_GetPhysicalCursorPos)(&local_18);
    iVar1 = FUN__text__0056ce80();
    if (iVar1 != 0) {
      iVar1 = FUN__text__00414400();
      if (iVar1 != 0) {
        (*API_USER32_DLL_ScreenToClient)(PTR_DAT_007a0bb4,&local_18);
        FUN__text__0056ce80();
      }
      local_8[0x22d] = local_18;
      local_8[0x22e] = local_14;
    }
    local_8[0x231] = local_8[0x43];
    local_8[0x232] = local_8[0x44];
    local_8[0x233] = local_8[0x45];
    local_8[0x234] = local_8[0x235];
    local_8[0x235] = 0;
    if ((*(byte *)(local_8 + 0x46) & 0x80) != 0) {
      local_8[0x235] = local_8[0x235] | 1;
    }
    if ((*(byte *)((int)local_8 + 0x119) & 0x80) != 0) {
      local_8[0x235] = local_8[0x235] | 2;
    }
    if ((*(byte *)((int)local_8 + 0x11a) & 0x80) != 0) {
      local_8[0x235] = local_8[0x235] | 4;
    }
    local_8[0x236] = (local_8[0x234] ^ local_8[0x235]) & local_8[0x235];
    local_8[0x239] = (local_8[0x234] ^ local_8[0x235]) & local_8[0x234];
    local_8[0x237] = 0;
    FUN__text__00412390(local_8 + 0x255,1,8);
    FUN__text__00412390(local_8 + 0x25a,2,0x10);
    FUN__text__00412390(local_8 + 0x25f,4,0x20);
    local_8[0x238] = 0;
    FUN__text__004124f0(local_8 + 0x264,1,0x40);
    FUN__text__004124f0(local_8 + 0x269,2,0x80);
    FUN__text__004124f0(local_8 + 0x26e,4,0x100);
    FUN__text__00412650(local_8 + 0x240,1);
    FUN__text__00412650(local_8 + 0x247,2);
    FUN__text__00412650(local_8 + 0x24e,4);
    local_8[0x23a] = local_8[0x236];
    if ((local_8[0x235] == 0) || (local_8[0x235] != local_8[0x234])) {
      local_8[0x23e] = 0;
      local_8[0x23d] = 0;
    }
    else {
      if (local_8[0x23e] == 0) {
        if (local_8[0x23b] <= local_8[0x23d]) {
          local_8[0x23e] = 1;
          local_8[0x23d] = 0;
          local_8[0x23a] = local_8[0x235];
        }
      }
      else if (local_8[0x23c] <= local_8[0x23d]) {
        local_8[0x23e] = 1;
        local_8[0x23d] = 0;
        local_8[0x23a] = local_8[0x235];
      }
      local_8[0x23d] = local_8[0x23d] + 1;
    }
  }
  local_8 = (int *)0x41227f;
  FUN__text__0056ce80();
  return;
}

