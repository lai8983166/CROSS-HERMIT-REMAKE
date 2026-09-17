
void __fastcall FUN_0040d610(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 8) + 0x14))(*(undefined4 *)(param_1 + 8),0,0,0,0);
    local_c = __chkesp();
    if (local_c < 0) {
      FUN_0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",DAT_005ff140 + 9,
                   local_c,"AllStopPlay()",1);
    }
    FUN_0040c140();
  }
  local_8 = 0x40d6af;
  __chkesp();
  return;
}

