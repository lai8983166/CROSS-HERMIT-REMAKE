
void __fastcall FUN_004246c0(undefined4 *param_1)

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
  *param_1 = &PTR_mdi_frame_proc_00594aa8;
  local_8 = param_1;
  FUN_00424700();
  local_8 = (undefined4 *)0x4246fb;
  __chkesp();
  return;
}

