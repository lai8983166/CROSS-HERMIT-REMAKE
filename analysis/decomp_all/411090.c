
void __fastcall FUN__text__00411090(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_28 = param_1[0x22d];
    local_24 = param_1[0x22e];
    local_8 = param_1;
    (*API_USER32_DLL_ClientToScreen)(PTR_DAT_007a0bb4,&local_28);
    FUN__text__0056ce80();
    (*API_USER32_DLL_SetPhysicalCursorPos)(local_28,local_24);
    FUN__text__0056ce80();
    FUN__text__00412290(local_8 + 0x273);
    (**(code **)(*(int *)*local_8 + 0xc))(*local_8,&DAT_005cc05c,local_8 + 2,0);
    local_20 = FUN__text__0056ce80();
    if (local_20 == 0) {
      (**(code **)(*(int *)local_8[2] + 0x2c))(local_8[2],&DAT_005cae44);
      local_20 = FUN__text__0056ce80();
      if (local_20 == 0) {
        (**(code **)(*(int *)local_8[2] + 0x34))(local_8[2],PTR_DAT_007a0bb4,6);
        local_20 = FUN__text__0056ce80();
        if (local_20 == 0) {
          local_1c = 0x14;
          local_18 = 0x10;
          local_14 = 0;
          local_10 = 0;
          local_c = 1;
          (**(code **)(*(int *)local_8[2] + 0x18))(local_8[2],2,&local_1c);
          local_20 = FUN__text__0056ce80();
          if (local_20 == 0) {
            _memset(local_8 + 0x48,0,0x244);
            local_8[0x48] = 0x244;
            (**(code **)(*(int *)local_8[2] + 0x3c))(local_8[2],local_8 + 0x48);
            local_20 = FUN__text__0056ce80();
            (**(code **)(*(int *)local_8[2] + 0x1c))(local_8[2]);
            local_20 = FUN__text__0056ce80();
          }
        }
      }
    }
  }
  local_8 = (int *)0x41128a;
  FUN__text__0056ce80();
  return;
}

