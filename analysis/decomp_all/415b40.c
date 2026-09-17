
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall timing_fn_E(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined8 uVar4;
  undefined4 auStack_64 [16];
  undefined8 uStack_24;
  int iStack_1c;
  int iStack_18;
  int *piStack_14;
  double dStack_10;
  undefined *puStack_8;
  
  puVar3 = auStack_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  piStack_14 = (int *)(param_1 + 0xb188);
  puStack_8 = (undefined *)param_1;
  if (*piStack_14 == 0 && *(int *)(param_1 + 0xb18c) == 0) {
    (*API_WINMM_DLL_timeGetTime)();
    uVar1 = __chkesp();
    *(undefined4 *)((int)puStack_8 + 0xb1a8) = uVar1;
    *(undefined4 *)((int)puStack_8 + 0xb1ac) = 0;
    *(int *)((int)puStack_8 + 0xb1c4) = *(int *)((int)puStack_8 + 0xb1c4) + 1;
    iStack_1c = *(uint *)((int)puStack_8 + 0xb1a8) - *(uint *)((int)puStack_8 + 0xb1b0);
    iStack_18 = (*(int *)((int)puStack_8 + 0xb1ac) - *(int *)((int)puStack_8 + 0xb1b4)) -
                (uint)(*(uint *)((int)puStack_8 + 0xb1a8) < *(uint *)((int)puStack_8 + 0xb1b0));
    dStack_10 = (double)CONCAT44(iStack_18,iStack_1c);
    uStack_24 = CONCAT44(uStack_24._4_4_,(undefined4)uStack_24);
    if (_DAT_00592d68 <= dStack_10) {
      *(uint *)((int)puStack_8 + 0xb1b8) =
           *(uint *)((int)puStack_8 + 0xb1a8) - *(uint *)((int)puStack_8 + 0xb1b0);
      *(uint *)((int)puStack_8 + 0xb1bc) =
           (*(int *)((int)puStack_8 + 0xb1ac) - *(int *)((int)puStack_8 + 0xb1b4)) -
           (uint)(*(uint *)((int)puStack_8 + 0xb1a8) < *(uint *)((int)puStack_8 + 0xb1b0));
      *(undefined4 *)((int)puStack_8 + 0xb1c8) = *(undefined4 *)((int)puStack_8 + 0xb1c0);
      *(undefined4 *)((int)puStack_8 + 0xb1cc) = *(undefined4 *)((int)puStack_8 + 0xb1c4);
      *(undefined4 *)((int)puStack_8 + 0xb1b0) = *(undefined4 *)((int)puStack_8 + 0xb1a8);
      *(undefined4 *)((int)puStack_8 + 0xb1b4) = *(undefined4 *)((int)puStack_8 + 0xb1ac);
      *(undefined4 *)((int)puStack_8 + 0xb1c0) = 0;
      *(undefined4 *)((int)puStack_8 + 0xb1c4) = 0;
      uStack_24 = CONCAT44(uStack_24._4_4_,(undefined4)uStack_24);
    }
  }
  else {
    (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1 + 0xb1a8);
    __chkesp();
    *(int *)((int)puStack_8 + 0xb1c4) = *(int *)((int)puStack_8 + 0xb1c4) + 1;
    uStack_24 = func_0x0056dcf0(*(uint *)((int)puStack_8 + 0xb1a8) -
                                *(uint *)((int)puStack_8 + 0xb1b0),
                                (*(int *)((int)puStack_8 + 0xb1ac) -
                                *(int *)((int)puStack_8 + 0xb1b4)) -
                                (uint)(*(uint *)((int)puStack_8 + 0xb1a8) <
                                      *(uint *)((int)puStack_8 + 0xb1b0)),
                                *(undefined4 *)((int)puStack_8 + 0xb188),
                                *(undefined4 *)((int)puStack_8 + 0xb18c));
    dStack_10 = (double)uStack_24 * _DAT_00592d40;
    if (_DAT_00592d40 <= dStack_10) {
      uVar4 = func_0x0056cfcc();
      *(undefined8 *)((int)puStack_8 + 0xb1b8) = uVar4;
      *(undefined4 *)((int)puStack_8 + 0xb1c8) = *(undefined4 *)((int)puStack_8 + 0xb1c0);
      *(undefined4 *)((int)puStack_8 + 0xb1cc) = *(undefined4 *)((int)puStack_8 + 0xb1c4);
      *(undefined4 *)((int)puStack_8 + 0xb1b0) = *(undefined4 *)((int)puStack_8 + 0xb1a8);
      *(undefined4 *)((int)puStack_8 + 0xb1b4) = *(undefined4 *)((int)puStack_8 + 0xb1ac);
      *(undefined4 *)((int)puStack_8 + 0xb1c0) = 0;
      *(undefined4 *)((int)puStack_8 + 0xb1c4) = 0;
    }
  }
  puStack_8 = &UNK_00415d81;
  __chkesp();
  return;
}

