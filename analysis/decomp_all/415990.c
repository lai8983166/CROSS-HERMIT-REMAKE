
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall timing_fn_D(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_74 [16];
  int iStack_34;
  int iStack_30;
  int iStack_2c;
  int iStack_28;
  int *piStack_24;
  double dStack_20;
  double dStack_18;
  uint uStack_10;
  int iStack_c;
  undefined *puStack_8;
  
  puVar2 = auStack_74;
  for (iVar1 = 0x1c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0xb1d0) != 0) {
    piStack_24 = (int *)(param_1 + 0xb188);
    puStack_8 = (undefined *)param_1;
    if (*piStack_24 == 0 && *(int *)(param_1 + 0xb18c) == 0) {
      (*API_WINMM_DLL_timeGetTime)();
      uStack_10 = __chkesp();
      iStack_c = 0;
      iStack_2c = uStack_10 - *(uint *)((int)puStack_8 + 0xb1d8);
      iStack_28 = -(uint)(uStack_10 < *(uint *)((int)puStack_8 + 0xb1d8)) -
                  *(int *)((int)puStack_8 + 0xb1dc);
      dStack_18 = (double)CONCAT44(iStack_28,iStack_2c);
    }
    else {
      (*API_KERNEL32_DLL_QueryPerformanceCounter)(&uStack_10);
      __chkesp();
      iStack_34 = uStack_10 - *(uint *)((int)puStack_8 + 0xb1d8);
      iStack_30 = (iStack_c - *(int *)((int)puStack_8 + 0xb1dc)) -
                  (uint)(uStack_10 < *(uint *)((int)puStack_8 + 0xb1d8));
      dStack_18 = ((double)CONCAT44(iStack_30,iStack_34) /
                  (double)*(longlong *)((int)puStack_8 + 0xb188)) * _DAT_00592d40;
    }
    dStack_20 = (double)*(longlong *)((int)puStack_8 + 0xb1e8);
  }
  puStack_8 = &UNK_00415a8c;
  __chkesp();
  return;
}

