
void __thiscall FUN__text__0042bff0(int param_1,undefined4 param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(uint *)(param_1 + 0x2c) & 2) == 0) {
    local_10 = *(int *)(param_1 + 0x18);
    local_14 = *(int *)(param_1 + 0x1c);
  }
  else {
    local_10 = ((int)*(short *)(param_1 + 0x30) * *(int *)(param_1 + 0x18)) / 100;
    local_14 = ((int)*(short *)(param_1 + 0x32) * *(int *)(param_1 + 0x1c)) / 100;
  }
  if ((*(uint *)(param_1 + 0x2c) & 1) != 0) {
    param_3 = param_3 - local_10 / 2;
    param_4 = param_4 - local_14 / 2;
  }
  local_8 = param_1;
  if ((local_10 == *(int *)(param_1 + 0x18)) && (local_14 == *(int *)(param_1 + 0x1c))) {
    local_c = FUN__text__00420610(param_2,*(undefined4 *)(param_1 + 0x28),param_3,param_4);
  }
  else {
    local_c = FUN__text__00420830(param_2,param_3,param_4,local_10,local_14);
  }
  local_8 = 0x42c0f6;
  FUN__text__0056ce80();
  return;
}

