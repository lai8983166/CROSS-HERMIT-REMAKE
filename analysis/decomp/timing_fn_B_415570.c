
/* WARNING: Stack frame is not setup normally: Input value of stackpointer is not used */

void timing_fn_B(void)

{
  code *pcVar1;
  char in_AL;
  undefined4 uVar2;
  int *piVar3;
  int *unaff_EBP;
  int iVar4;
  
  pcVar1 = API_WINMM_DLL_timeGetTime;
  iVar4 = *unaff_EBP;
  if (in_AL == '|') {
    *unaff_EBP = (int)&UNK_0041557e;
    (*pcVar1)();
    unaff_EBP[-1] = (int)&UNK_00415585;
    uVar2 = __chkesp();
    iVar4 = *(int *)(iVar4 + -4);
    *(undefined4 *)(iVar4 + 0xb1e0) = uVar2;
    *(undefined4 *)(iVar4 + 0xb1e4) = 0;
  }
  else {
    *unaff_EBP = *(int *)(iVar4 + -4) + 0xb1e0;
    pcVar1 = API_KERNEL32_DLL_QueryPerformanceCounter;
    piVar3 = unaff_EBP + -1;
    unaff_EBP = unaff_EBP + -1;
    *piVar3 = (int)&UNK_004155aa;
    (*pcVar1)();
    *(undefined **)((int)unaff_EBP + -4) = &UNK_004155b1;
    uVar2 = __chkesp();
    *(undefined4 *)(iVar4 + -8) = uVar2;
  }
  *(undefined **)((int)unaff_EBP + 0x54) = &UNK_004155c1;
  __chkesp();
  return;
}

