
int FUN__text1__00847af0(int param_1,int param_2,int param_3)

{
  uint uVar1;
  undefined4 uVar2;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = *(int *)(param_2 + 0xc);
  uVar1 = *(uint *)(param_1 + 0x30);
  if (*(uint *)(param_1 + 0x34) < uVar1) {
    local_14 = *(int *)(param_1 + 0x2c);
  }
  else {
    local_14 = *(int *)(param_1 + 0x34);
  }
  local_10 = local_14 - uVar1;
  if (*(uint *)(param_2 + 0x10) < local_10) {
    local_10 = *(uint *)(param_2 + 0x10);
  }
  if ((local_10 != 0) && (param_3 == -5)) {
    param_3 = 0;
  }
  *(uint *)(param_2 + 0x10) = *(int *)(param_2 + 0x10) - local_10;
  *(uint *)(param_2 + 0x14) = *(int *)(param_2 + 0x14) + local_10;
  if (*(int *)(param_1 + 0x38) != 0) {
    uVar2 = (**(code **)(param_1 + 0x38))(*(undefined4 *)(param_1 + 0x3c),uVar1,local_10);
    *(undefined4 *)(param_1 + 0x3c) = uVar2;
    *(undefined4 *)(param_2 + 0x30) = *(undefined4 *)(param_1 + 0x3c);
  }
  FUN__text1__00848490(local_8,uVar1,local_10);
  local_8 = local_8 + local_10;
  local_c = uVar1 + local_10;
  if (local_c == *(int *)(param_1 + 0x2c)) {
    local_c = *(int *)(param_1 + 0x28);
    if (*(int *)(param_1 + 0x34) == *(int *)(param_1 + 0x2c)) {
      *(undefined4 *)(param_1 + 0x34) = *(undefined4 *)(param_1 + 0x28);
    }
    local_10 = *(int *)(param_1 + 0x34) - local_c;
    if (*(uint *)(param_2 + 0x10) < local_10) {
      local_10 = *(uint *)(param_2 + 0x10);
    }
    if ((local_10 != 0) && (param_3 == -5)) {
      param_3 = 0;
    }
    *(uint *)(param_2 + 0x10) = *(int *)(param_2 + 0x10) - local_10;
    *(uint *)(param_2 + 0x14) = *(int *)(param_2 + 0x14) + local_10;
    if (*(int *)(param_1 + 0x38) != 0) {
      uVar2 = (**(code **)(param_1 + 0x38))(*(undefined4 *)(param_1 + 0x3c),local_c,local_10);
      *(undefined4 *)(param_1 + 0x3c) = uVar2;
      *(undefined4 *)(param_2 + 0x30) = *(undefined4 *)(param_1 + 0x3c);
    }
    FUN__text1__00848490(local_8,local_c,local_10);
    local_8 = local_8 + local_10;
    local_c = local_c + local_10;
  }
  *(int *)(param_2 + 0xc) = local_8;
  *(int *)(param_1 + 0x30) = local_c;
  return param_3;
}

