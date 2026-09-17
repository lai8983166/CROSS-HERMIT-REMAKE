
void __fastcall FUN_00410cb0(int *param_1)

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
    (**(code **)(*(int *)param_1[1] + 0x20))(param_1[1]);
    __chkesp();
  }
  if (local_8[2] != 0) {
    (**(code **)(*(int *)local_8[2] + 0x20))(local_8[2]);
    __chkesp();
  }
  if (local_8[1] != 0) {
    (**(code **)(*(int *)local_8[1] + 8))(local_8[1]);
    __chkesp();
    local_8[1] = 0;
  }
  if (local_8[2] != 0) {
    (**(code **)(*(int *)local_8[2] + 8))(local_8[2]);
    __chkesp();
    local_8[2] = 0;
  }
  if (*local_8 != 0) {
    (**(code **)(*(int *)*local_8 + 8))(*local_8);
    __chkesp();
    *local_8 = 0;
  }
  local_8 = (int *)0x410daa;
  __chkesp();
  return;
}

