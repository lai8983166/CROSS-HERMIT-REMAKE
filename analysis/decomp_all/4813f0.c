
void __thiscall FUN__text__004813f0(int param_1,int param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  short local_1c;
  int local_18;
  int local_14;
  undefined1 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_20 = param_1 + 0x108f48;
  local_18 = param_3 - param_4;
  if (8 < local_18) {
    local_18 = 8;
  }
  local_8 = param_1;
  local_c = FUN__text__00427d60();
  if (local_c == 0) {
    iVar2 = FUN__text__00424f80("list!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                DAT_00618ec8 + 0xd,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = *(undefined1 **)(local_c + 8);
  local_10[1] = *(undefined1 *)(param_2 + 2);
  if (param_4 < 8) {
    *local_10 = 0xb;
  }
  else {
    *local_10 = 0xc;
  }
  local_10[2] = (undefined1)param_3;
  local_10[3] = (undefined1)local_18;
  local_10[4] = 0;
  for (local_14 = 0; local_14 != 8; local_14 = local_14 + 1) {
    local_10[local_14 + 5] = 0;
  }
  for (local_14 = 0; local_14 != local_18; local_14 = local_14 + 1) {
    if (*(short *)(local_20 + 2 + (param_4 + local_14) * 2) == -1) {
      local_1c = 0;
    }
    else {
      local_1c = *(short *)(local_20 + 2 + (param_4 + local_14) * 2) + 1;
    }
    local_10[4] = local_10[4] |
                  (byte)((int)((int)local_1c & 0x100U) >> ((char)local_14 + 1U & 0x1f));
    local_10[local_14 + 5] = (char)local_1c;
  }
  FUN__text__00427e30(local_c);
  local_8 = 0x481572;
  FUN__text__0056ce80();
  return;
}

