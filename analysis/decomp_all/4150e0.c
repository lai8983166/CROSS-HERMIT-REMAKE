
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall timing_fn_A(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_78 [16];
  char cStack_38;
  int iStack_34;
  int iStack_30;
  char cStack_2c;
  int iStack_28;
  int iStack_24;
  int *piStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  uint uStack_14;
  double dStack_10;
  undefined *puStack_8;
  
  puVar3 = auStack_78;
  for (iVar2 = 0x1d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  piStack_20 = (int *)(param_1 + 0xb188);
  puStack_8 = (undefined *)param_1;
  if (*piStack_20 == 0 && *(int *)(param_1 + 0xb18c) == 0) {
    (*API_WINMM_DLL_timeGetTime)();
    uVar1 = __chkesp();
    *(undefined4 *)((int)puStack_8 + 0xb190) = uVar1;
    *(undefined4 *)((int)puStack_8 + 0xb194) = 0;
    iStack_28 = *(uint *)((int)puStack_8 + 0xb190) - *(uint *)((int)puStack_8 + 0xb198);
    iStack_24 = (*(int *)((int)puStack_8 + 0xb194) - *(int *)((int)puStack_8 + 0xb19c)) -
                (uint)(*(uint *)((int)puStack_8 + 0xb190) < *(uint *)((int)puStack_8 + 0xb198));
    dStack_10 = (double)CONCAT44(iStack_24,iStack_28);
    cStack_2c = *(char *)((int)puStack_8 + 0xb17c);
    if (cStack_2c == '\x01') {
      uStack_14 = 0x40408000;
    }
    else if (cStack_2c == '\x02') {
      uStack_14 = 0x40490000;
    }
    else if (cStack_2c == '\x03') {
      uStack_14 = 0x40508000;
    }
    else {
      uStack_14 = 0x40300000;
    }
  }
  else {
    (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1 + 0xb190);
    uStack_1c = __chkesp();
    iStack_34 = *(uint *)((int)puStack_8 + 0xb190) - *(uint *)((int)puStack_8 + 0xb198);
    iStack_30 = (*(int *)((int)puStack_8 + 0xb194) - *(int *)((int)puStack_8 + 0xb19c)) -
                (uint)(*(uint *)((int)puStack_8 + 0xb190) < *(uint *)((int)puStack_8 + 0xb198));
    dStack_10 = ((double)CONCAT44(iStack_30,iStack_34) /
                (double)*(longlong *)((int)puStack_8 + 0xb188)) * _DAT_00592d40;
    cStack_38 = *(char *)((int)puStack_8 + 0xb17c);
    if (cStack_38 == '\x01') {
      uStack_14 = 0x40e046a0;
    }
    else if (cStack_38 == '\x02') {
      uStack_14 = 0x40e86a00;
    }
    else if (cStack_38 == '\x03') {
      uStack_14 = 0x40f046a0;
    }
    else {
      uStack_14 = 0x40d04680;
    }
  }
  uStack_18 = 0;
  if ((double)((ulonglong)uStack_14 << 0x20) <= dStack_10) {
    *(undefined4 *)((int)puStack_8 + 0xb198) = *(undefined4 *)((int)puStack_8 + 0xb190);
    *(undefined4 *)((int)puStack_8 + 0xb19c) = *(undefined4 *)((int)puStack_8 + 0xb194);
  }
  puStack_8 = &UNK_004152b9;
  __chkesp();
  return;
}

