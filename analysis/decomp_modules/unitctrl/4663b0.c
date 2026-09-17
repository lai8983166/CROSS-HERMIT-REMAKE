
void FUN_004663b0(uint param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_00464cc0();
  if ((param_1 & 1) != 0) {
    FUN_00428ad0(local_8);
  }
  local_8 = 0x4663fb;
  __chkesp();
  return;
}

