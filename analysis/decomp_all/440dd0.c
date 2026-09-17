
void __thiscall FUN__text__00440dd0(int param_1,short *param_2,short *param_3)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *param_2 - *(short *)(param_1 + 0x2646c);
  local_10 = *param_3 - *(short *)(param_1 + 0x26470);
  local_14 = (int)local_c;
  local_8 = param_1;
  sVar1 = __ftol();
  *param_2 = sVar1;
  local_18 = (int)local_10;
  sVar1 = __ftol();
  *param_3 = sVar1;
  return;
}

