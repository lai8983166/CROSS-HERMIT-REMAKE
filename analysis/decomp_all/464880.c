
void __fastcall FUN_00464880(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN_00464980(param_1);
  FUN_00464980(local_8 + 0x12e8);
  local_8 = 0x4648ca;
  __chkesp();
  return;
}

