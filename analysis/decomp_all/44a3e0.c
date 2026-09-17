
void __thiscall FUN__text__0044a3e0(int param_1,short param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_84 [16];
  undefined4 local_44;
  short local_40;
  short local_3c;
  short local_38;
  short local_34;
  int local_30;
  int local_2c;
  undefined4 local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_84;
  for (iVar1 = 0x20; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x1a54;
  local_10 = param_1 + 0x1a88;
  local_14 = param_1 + 0x8a80 + *(char *)(param_1 + 0x1a8a) * 8;
  local_8 = param_1;
  local_1c = FUN__text__00428380();
  local_20 = FUN__text__00428350();
  local_24 = FUN__text__004283b0();
  local_28 = FUN__text__00428310();
  local_34 = param_2 + 0x242;
  local_38 = param_3 + 0x70;
  local_18 = local_8 + 0x1b8;
  local_30 = 0;
  for (local_2c = local_24; (local_2c != local_24 + local_20 && (local_2c < local_1c));
      local_2c = local_2c + 1) {
    local_3c = local_34;
    local_40 = local_38 + (short)local_30 * 0x11;
    local_44 = 0xffffffff;
    *(undefined2 *)(local_18 + 0x76 + local_2c * 0x80) = 0x48;
    FUN__text__00408f10(local_34 + 2,(int)local_40,0xffffffff);
    local_30 = local_30 + 1;
  }
  local_8 = 0x44a524;
  FUN__text__0056ce80();
  return;
}

