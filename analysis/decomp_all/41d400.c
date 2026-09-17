
void __fastcall FUN_0041d400(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (param_1[1] != 0) {
    (**(code **)(*(int *)param_1[1] + 0x24))(param_1[1]);
    __chkesp();
  }
  if (local_8[5] != 0) {
    (**(code **)(*(int *)local_8[5] + 0x34))(local_8[5],0,0,0);
    __chkesp();
  }
  if (local_8[5] != 0) {
    (**(code **)(*(int *)local_8[5] + 8))(local_8[5]);
    __chkesp();
    local_8[5] = 0;
  }
  if (local_8[7] != 0) {
    (**(code **)(*(int *)local_8[7] + 8))(local_8[7]);
    __chkesp();
    local_8[7] = 0;
  }
  if (local_8[4] != 0) {
    (**(code **)(*(int *)local_8[4] + 8))(local_8[4]);
    __chkesp();
    local_8[4] = 0;
  }
  if (local_8[3] != 0) {
    (**(code **)(*(int *)local_8[3] + 8))(local_8[3]);
    __chkesp();
    local_8[3] = 0;
  }
  if (local_8[2] != 0) {
    (**(code **)(*(int *)local_8[2] + 8))(local_8[2]);
    __chkesp();
    local_8[2] = 0;
  }
  if (local_8[1] != 0) {
    (**(code **)(*(int *)local_8[1] + 8))(local_8[1]);
    __chkesp();
    local_8[1] = 0;
  }
  if (*local_8 != 0) {
    (**(code **)(*(int *)*local_8 + 8))(*local_8);
    __chkesp();
    *local_8 = 0;
  }
  *(undefined1 *)(local_8 + 8) = 0;
  *(undefined1 *)((int)local_8 + 0x21) = 0;
  local_8 = (int *)0x41d5c6;
  __chkesp();
  return;
}

