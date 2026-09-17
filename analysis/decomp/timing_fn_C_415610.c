
/* WARNING: Removing unreachable block (ram,0x0041588b) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall timing_fn_C(int param_1)

{
  uint uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined8 uVar7;
  undefined4 auStack_88 [16];
  undefined8 uStack_48;
  undefined8 uStack_40;
  int iStack_38;
  char cStack_34;
  int iStack_30;
  int iStack_2c;
  char cStack_28;
  int iStack_24;
  int iStack_20;
  int *piStack_1c;
  undefined4 uStack_18;
  undefined4 uStack_14;
  double dStack_10;
  undefined *puStack_8;
  
  iVar5 = 0x21;
  puVar6 = auStack_88;
  while( true ) {
    if (iVar5 == 0) break;
    iVar5 = iVar5 + -1;
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  if (*(int *)(param_1 + 0xb1d0) != 0) {
    piStack_1c = (int *)(param_1 + 0xb188);
    puStack_8 = (undefined *)param_1;
    if (*piStack_1c == 0 && *(int *)(param_1 + 0xb18c) == 0) {
      (*API_WINMM_DLL_timeGetTime)();
      uVar4 = __chkesp();
      *(undefined4 *)((int)puStack_8 + 0xb1d8) = uVar4;
      *(undefined4 *)((int)puStack_8 + 0xb1dc) = 0;
      iStack_24 = *(uint *)((int)puStack_8 + 0xb1d8) - *(uint *)((int)puStack_8 + 0xb1e0);
      iStack_20 = (*(int *)((int)puStack_8 + 0xb1dc) - *(int *)((int)puStack_8 + 0xb1e4)) -
                  (uint)(*(uint *)((int)puStack_8 + 0xb1d8) < *(uint *)((int)puStack_8 + 0xb1e0));
      dStack_10 = (double)CONCAT44(iStack_20,iStack_24);
      cStack_28 = *(char *)((int)puStack_8 + 0xb17c);
      if (cStack_28 == '\x01') {
        uStack_14 = 0x40408000;
      }
      else if (cStack_28 == '\x02') {
        uStack_14 = 0x40490000;
      }
      else if (cStack_28 == '\x03') {
        uStack_14 = 0x40508000;
      }
      else {
        uStack_14 = 0x40300000;
      }
    }
    else {
      (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1 + 0xb1d8);
      __chkesp();
      iStack_30 = *(uint *)((int)puStack_8 + 0xb1d8) - *(uint *)((int)puStack_8 + 0xb1e0);
      iStack_2c = (*(int *)((int)puStack_8 + 0xb1dc) - *(int *)((int)puStack_8 + 0xb1e4)) -
                  (uint)(*(uint *)((int)puStack_8 + 0xb1d8) < *(uint *)((int)puStack_8 + 0xb1e0));
      dStack_10 = ((double)CONCAT44(iStack_2c,iStack_30) /
                  (double)*(longlong *)((int)puStack_8 + 0xb188)) * _DAT_00592d68 * _DAT_00592d68;
      cStack_34 = *(char *)((int)puStack_8 + 0xb17c);
      if (cStack_34 == '\x01') {
        uStack_14 = 0x40e046a0;
      }
      else if (cStack_34 == '\x02') {
        uStack_14 = 0x40e86a00;
      }
      else if (cStack_34 == '\x03') {
        uStack_14 = 0x40f046a0;
      }
      else {
        uStack_14 = 0x40d04680;
      }
    }
    puVar2 = puStack_8;
    uStack_18 = 0;
    *(undefined4 *)((int)puStack_8 + 0xb1e0) = *(undefined4 *)((int)puStack_8 + 0xb1d8);
    *(undefined4 *)((int)puStack_8 + 0xb1e4) = *(undefined4 *)((int)puStack_8 + 0xb1dc);
    uVar7 = func_0x0056cfcc();
    puVar3 = puStack_8;
    uVar1 = *(uint *)((int)puVar2 + 0xb1e8);
    iVar5 = *(int *)((int)puVar2 + 0xb1ec);
    *(uint *)((int)puStack_8 + 0xb1e8) = uVar1 + (uint)uVar7;
    *(uint *)((int)puStack_8 + 0xb1ec) =
         iVar5 + (int)((ulonglong)uVar7 >> 0x20) + (uint)CARRY4(uVar1,(uint)uVar7);
    uVar7 = func_0x0056cfcc();
    uVar1 = *(uint *)((int)puVar3 + 0xb1e8);
    iVar5 = *(int *)((int)puVar3 + 0xb1ec);
    *(uint *)((int)puStack_8 + 0xb1e8) = uVar1 - (uint)uVar7;
    *(uint *)((int)puStack_8 + 0xb1ec) =
         (iVar5 - (int)((ulonglong)uVar7 >> 0x20)) - (uint)(uVar1 < (uint)uVar7);
    iStack_38 = (int)puStack_8 + 0xb1e8;
    if (*(int *)((int)puStack_8 + 0xb1ec) < 0) {
      uStack_40 = func_0x0056dcb0(*(undefined4 *)((int)puStack_8 + 0xb1e8),
                                  *(undefined4 *)((int)puStack_8 + 0xb1ec),0xffffffff,0xffffffff);
      if (uStack_40 < 1000000) {
        uStack_48 = func_0x0056dcb0(*(undefined4 *)((int)puStack_8 + 0xb1e8),
                                    *(undefined4 *)((int)puStack_8 + 0xb1ec),0xffffffff,0xffffffff);
        if (((double)CONCAT44(uStack_14,uStack_18) <= (double)uStack_48) &&
           (*(int *)((int)puStack_8 + 0xb1f4) < *(int *)((int)puStack_8 + 0xb1f0))) {
          *(int *)((int)puStack_8 + 0xb1f4) = *(int *)((int)puStack_8 + 0xb1f4) + 1;
        }
      }
      else {
        *(undefined4 *)((int)puStack_8 + 0xb1e8) = 0;
        *(undefined4 *)((int)puStack_8 + 0xb1ec) = 0;
      }
    }
    else {
      func_0x00415930();
    }
  }
  puStack_8 = &UNK_00415922;
  __chkesp();
  return;
}

