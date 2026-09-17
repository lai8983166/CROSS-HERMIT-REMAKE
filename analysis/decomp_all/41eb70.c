
void __fastcall FUN_0041eb70(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1[3] != 0) {
    local_8 = param_1;
    FUN_0041f4e0(param_1[4]);
    local_8[4] = 0xffffffff;
    *local_8 = 0;
    local_8[1] = 0;
    *(undefined1 *)(local_8 + 2) = 0xff;
    local_8[3] = 0;
  }
  local_8 = (undefined4 *)0x41ebe5;
  __chkesp();
  return;
}

