
void __fastcall FUN_00465e60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x117c40) != 0) {
    local_c = *(undefined4 *)(param_1 + 0x117c40);
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x117c40) = 0;
  }
  FUN_00493e60();
  FUN_00467320();
  FUN_00467660();
  FUN_004674c0();
  FUN_004677f0();
  FUN_00493860();
  FUN_0040bb90();
  FUN_004662b0();
  FUN_00466f00();
  FUN_0043a320();
  if (*(int *)(local_8 + 0xdb80c) != 0) {
    (*API_GDI32_DLL_DeleteObject)(*(undefined4 *)(local_8 + 0xdb80c));
    __chkesp();
    *(undefined4 *)(local_8 + 0xdb80c) = 0;
  }
  if (*(int *)(local_8 + 0xdb810) != 0) {
    (*API_GDI32_DLL_DeleteObject)(*(undefined4 *)(local_8 + 0xdb810));
    __chkesp();
    *(undefined4 *)(local_8 + 0xdb810) = 0;
  }
  local_8 = 0x465f7d;
  __chkesp();
  return;
}

