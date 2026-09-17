
void FUN__text__00472370(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(short *)(*(int *)(param_1 + 600) + 0x16) == 0) ||
     ((*(short *)(*(int *)(param_1 + 600) + 0x16) != 0 &&
      (*(short *)(*(int *)(param_1 + 600) + 0x14) <= *(short *)(*(int *)(param_1 + 600) + 0x16)))))
  {
    *(undefined2 *)(param_1 + 0x504) = 0;
  }
  else {
    *(short *)(param_1 + 0x504) = *(short *)(param_1 + 0x504) + 1;
    local_c = (int)*(short *)(*(int *)(param_1 + 600) + 0x18) - (int)*(short *)(param_1 + 0x508);
    iVar1 = FUN__text__00469220(param_1);
    if (iVar1 != 0) {
      local_c = (local_c * 0x32) / 100;
    }
    if (local_c < 0) {
      local_c = 1;
    }
    if (local_c <= *(short *)(param_1 + 0x504)) {
      *(undefined2 *)(param_1 + 0x504) = 0;
      FUN__text__00472550(param_1,0,1);
    }
  }
  if ((*(short *)(*(int *)(param_1 + 600) + 0x1c) == 0) ||
     (*(short *)(*(int *)(param_1 + 600) + 0x1c) < *(short *)(*(int *)(param_1 + 600) + 0x1a))) {
    *(short *)(param_1 + 0x506) = *(short *)(param_1 + 0x506) + 1;
    local_c = (int)*(short *)(*(int *)(param_1 + 600) + 0x1e) - (int)*(short *)(param_1 + 0x50a);
    iVar1 = FUN__text__00469220(param_1);
    if (iVar1 != 0) {
      local_c = (local_c * 200) / 100;
    }
    if (local_c < 0) {
      local_c = 1;
    }
    if (local_c <= *(short *)(param_1 + 0x506)) {
      *(undefined2 *)(param_1 + 0x506) = 0;
      FUN__text__00472550(param_1,1,1);
    }
  }
  else {
    *(undefined2 *)(param_1 + 0x506) = 0;
  }
  local_8 = 0x472548;
  FUN__text__0056ce80();
  return;
}

