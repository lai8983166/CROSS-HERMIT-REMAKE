
void __thiscall
mdi_frame_proc(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
              undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_48 [16];
  undefined *puStack_8;
  
  puVar2 = auStack_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  puStack_8 = (undefined *)param_1;
  if (*(int *)(param_1 + 8) == 0) {
    if (*(int *)(param_1 + 0xc) == 0) {
      (*API_NTDLL_DLL_NtdllDefWindowProc_A)(param_2,param_3,param_4,param_5);
      __chkesp();
    }
  }
  else {
    (*API_USER32_DLL_CallWindowProcA)(*(undefined4 *)(param_1 + 8),param_2,param_3,param_4,param_5);
    __chkesp();
  }
  puStack_8 = &UNK_00424b17;
  __chkesp();
  return;
}

