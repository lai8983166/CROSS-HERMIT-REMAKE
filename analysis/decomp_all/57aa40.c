
void FUN_0057aa40(undefined **param_1)

{
  (*API_KERNEL32_DLL_VirtualFree)(param_1[4],0,0x8000);
  if ((undefined **)PTR_LOOP_00764158 == param_1) {
    PTR_LOOP_00764158 = param_1[1];
  }
  if (param_1 == &PTR_LOOP_00762138) {
    DAT_00762148 = 0xffffffff;
  }
  else {
    *(undefined **)param_1[1] = *param_1;
    *(undefined **)(*param_1 + 4) = param_1[1];
    (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,param_1);
  }
  return;
}

