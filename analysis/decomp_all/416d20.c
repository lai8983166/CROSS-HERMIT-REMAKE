
void __thiscall FUN__text__00416d20(int param_1,undefined4 param_2,int param_3,uint param_4)

{
  short sVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (param_3 == 0x100) {
    local_8 = param_1;
    FUN__text__00416c40(param_2);
  }
  else {
    sVar2 = (short)param_3;
    if (param_3 < 0x101) {
      for (local_c = 0; local_c != 0x100; local_c = local_c + 1) {
        sVar1 = (short)local_c;
        if ((param_4 & 4) == 0) {
          *(short *)(param_1 + 0xb408 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb408 + local_c * 2) = sVar2 * sVar1;
        }
        if ((param_4 & 2) == 0) {
          *(short *)(param_1 + 0xb608 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb608 + local_c * 2) = sVar2 * sVar1;
        }
        if ((param_4 & 1) == 0) {
          *(short *)(param_1 + 0xb808 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb808 + local_c * 2) = sVar2 * sVar1;
        }
      }
    }
    else {
      for (local_c = 0; local_c != 0x100; local_c = local_c + 1) {
        sVar1 = (short)local_c;
        if ((param_4 & 4) == 0) {
          *(short *)(param_1 + 0xb408 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb408 + local_c * 2) = -1 - (0x200 - sVar2) * (0xff - sVar1);
        }
        if ((param_4 & 2) == 0) {
          *(short *)(param_1 + 0xb608 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb608 + local_c * 2) = -1 - (0x200 - sVar2) * (0xff - sVar1);
        }
        if ((param_4 & 1) == 0) {
          *(short *)(param_1 + 0xb808 + local_c * 2) = (short)(local_c << 8);
        }
        else {
          *(short *)(param_1 + 0xb808 + local_c * 2) = -1 - (0x200 - sVar2) * (0xff - sVar1);
        }
      }
    }
  }
  local_8 = 0x416f58;
  FUN__text__0056ce80();
  return;
}

