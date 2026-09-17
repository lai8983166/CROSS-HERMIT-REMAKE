
void FUN_0040bfa0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN_0040d330();
  if (*(int *)(local_8 + 0xc) != 0) {
    (**(code **)(**(int **)(local_8 + 0xc) + 8))(*(undefined4 *)(local_8 + 0xc));
    __chkesp();
    *(undefined4 *)(local_8 + 0xc) = 0;
  }
  if (*(int *)(local_8 + 0x10) != 0) {
    (**(code **)(**(int **)(local_8 + 0x10) + 8))(*(undefined4 *)(local_8 + 0x10));
    __chkesp();
    *(undefined4 *)(local_8 + 0x10) = 0;
  }
  if (*(int *)(local_8 + 8) != 0) {
    (**(code **)(**(int **)(local_8 + 8) + 0x14))(*(undefined4 *)(local_8 + 8),0,0,0,0);
    local_c = __chkesp();
    (**(code **)(**(int **)(local_8 + 8) + 0x98))(*(undefined4 *)(local_8 + 8));
    local_c = __chkesp();
    if ((local_c < 0) &&
       (iVar2 = FUN_00424f80(&DAT_005924d4,
                             "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                             DAT_005ff118 + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*(int *)(local_8 + 8) != 0) {
    (**(code **)(**(int **)(local_8 + 8) + 8))(*(undefined4 *)(local_8 + 8));
    __chkesp();
    *(undefined4 *)(local_8 + 8) = 0;
  }
  local_8 = 0x40c0e1;
  __chkesp();
  return;
}

