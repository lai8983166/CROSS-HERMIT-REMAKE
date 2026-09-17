
void __thiscall FUN__text__00418f70(int *param_1,undefined4 param_2,int param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_a4 [16];
  int local_64;
  undefined4 local_60;
  int local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  int local_30;
  int local_28;
  undefined4 local_18;
  int *local_8;
  
  puVar2 = local_a4;
  for (iVar1 = 0x28; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && ((char)param_1[0x5dc] == '\0')) {
    local_60 = 0;
    local_8 = param_1;
    iVar1 = FUN__text__004195e0(param_2);
    if (iVar1 == 0) {
      local_8[0x5da] = param_3;
      _memset(&local_58,0,0x50);
      local_58 = 0x50;
      local_40 = DAT_00592dd8;
      local_3c = DAT_00592ddc;
      local_38 = DAT_00592de0;
      local_34 = DAT_00592de4;
      local_54 = 0x1040;
      local_30 = local_8[0x5da];
      local_28 = local_8[0x5d8];
      local_18 = param_4;
      FUN__text__00418b20();
      (**(code **)(*(int *)*local_8 + 0x60))(*local_8,&local_58,2);
      local_64 = FUN__text__0056ce80();
      local_5c = local_64;
      if (local_64 == -0x7788fee8) {
        local_60 = 2;
      }
      else {
        if (local_64 == 0) {
          local_8[0x5db] = 0;
          *(undefined1 *)(local_8 + 0x5dc) = 1;
          goto LAB__text__004190d6;
        }
        local_60 = 1;
      }
    }
    FUN__text__00419710();
    local_8[0x5db] = -1;
    *(undefined1 *)(local_8 + 0x5dc) = 0;
  }
LAB__text__004190d6:
  local_8 = (int *)0x4190e6;
  FUN__text__0056ce80();
  return;
}

