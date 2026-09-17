
void __thiscall FUN__text__004190f0(int *param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int *local_c;
  int *local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*param_1 != 0) && ((char)param_1[0x5dc] == '\0')) && (param_2 < param_1[0x91])) {
    local_14 = 0;
    local_c = param_1 + param_2 * 0x15 + 0x94;
    local_c[0x11] = param_3;
    local_8 = param_1;
    (**(code **)(*(int *)*param_1 + 0x60))(*param_1,local_c,1);
    local_18 = FUN__text__0056ce80();
    local_10 = local_18;
    if (local_18 == -0x7788fee8) {
      local_14 = 2;
    }
    else {
      if (local_18 == 0) {
        iVar1 = FUN__text__004195e0(local_c[0xc]);
        if (iVar1 == 0) {
          local_8[0x5da] = local_8[param_2 * 0x15 + 0x9e];
          local_8[0x5db] = 1;
          *(undefined1 *)(local_8 + 0x5dc) = 1;
          FUN__text__0041ab10();
          goto LAB__text__00419225;
        }
        FUN__text__00419240();
      }
      FUN__text__0041b4a0(local_10);
      local_14 = 1;
    }
  }
LAB__text__00419225:
  local_8 = (int *)0x419232;
  FUN__text__0056ce80();
  return;
}

