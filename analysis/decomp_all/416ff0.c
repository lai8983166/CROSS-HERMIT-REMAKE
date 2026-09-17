
void FUN__text__00416ff0(uint *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1 + 2);
  FUN__text__0056ce80();
  param_1[4] = param_1[2] - *param_1;
  param_1[5] = (param_1[3] - param_1[1]) - (uint)(param_1[2] < *param_1);
  uStack_c = 0x41704a;
  FUN__text__0056ce80();
  return;
}

