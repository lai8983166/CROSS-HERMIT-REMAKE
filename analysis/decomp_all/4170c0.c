
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void timing_fn_F(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  bool bVar3;
  float10 fVar4;
  longlong lVar5;
  undefined4 auStack_ac [16];
  float fStack_6c;
  float fStack_68;
  float fStack_64;
  uint uStack_60;
  undefined4 uStack_5c;
  float fStack_58;
  float fStack_54;
  int iStack_50;
  int iStack_4c;
  float fStack_48;
  int iStack_44;
  int iStack_40;
  double dStack_3c;
  undefined8 uStack_34;
  double dStack_2c;
  uint uStack_24;
  int iStack_20;
  double dStack_1c;
  double dStack_14;
  undefined4 uStack_c;
  undefined *puStack_8;
  
  puVar2 = auStack_ac;
  for (iVar1 = 0x2a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (DAT_00799ad0 == 0) {
    DAT_00799ad0 = 1;
    (*API_KERNEL32_DLL_QueryPerformanceFrequency)(&uStack_c);
    DAT_00799ad4 = __chkesp();
    if (DAT_00799ad4 != 0) {
      DAT_00799ad8 = uStack_c;
      DAT_00799adc = puStack_8;
    }
  }
  if (DAT_00799ad4 == 0) {
    if (((_DAT_00799b08 == _DAT_00592d98) || (param_1 == 1)) || (param_1 == 4)) {
      (*API_WINMM_DLL_timeGetTime)();
      uStack_60 = __chkesp();
      uStack_5c = 0;
      uStack_34 = (double)uStack_60 * _DAT_00592d90;
    }
    else {
      uStack_34 = _DAT_00799b08;
    }
    lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    if (param_1 == 6) {
      dStack_3c = uStack_34 - (double)CONCAT44(_DAT_00799afc,_DAT_00799af8);
      _DAT_00799af8 = (undefined4)uStack_34;
      _DAT_00799afc = uStack_34._4_4_;
      fStack_64 = (float)dStack_3c;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 5) {
      fStack_68 = (float)((float10)uStack_34 - (float10)_DAT_00799b00);
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 0) {
      _DAT_00799b00 = uStack_34;
      _DAT_00799af8 = (undefined4)uStack_34;
      _DAT_00799afc = uStack_34._4_4_;
      _DAT_00799b08 = 0.0;
      DAT_005ff530 = 0;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 1) {
      if (DAT_005ff530 != 0) {
        _DAT_00799b00 = (uStack_34 - _DAT_00799b08) + _DAT_00799b00;
      }
      _DAT_00799b08 = 0.0;
      _DAT_00799af8 = (undefined4)uStack_34;
      _DAT_00799afc = uStack_34._4_4_;
      DAT_005ff530 = 0;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 2) {
      _DAT_00799b08 = uStack_34;
      _DAT_00799af8 = (undefined4)uStack_34;
      _DAT_00799afc = uStack_34._4_4_;
      DAT_005ff530 = 1;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 3) {
      _DAT_00799b08 = _DAT_00799b08 + _DAT_00592d88;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 4) {
      fStack_6c = (float)uStack_34;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
  }
  else {
    if (((DAT_00799ae0 == 0 && DAT_00799ae4 == 0) || (param_1 == 1)) || (param_1 == 4)) {
      (*API_KERNEL32_DLL_QueryPerformanceCounter)(&uStack_24);
      __chkesp();
    }
    else {
      uStack_24 = DAT_00799ae0;
      iStack_20 = DAT_00799ae4;
    }
    lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    if (param_1 == 6) {
      iStack_44 = uStack_24 - _DAT_00799ae8;
      iStack_40 = (iStack_20 - _DAT_00799aec) - (uint)(uStack_24 < _DAT_00799ae8);
      dStack_1c = (double)CONCAT44(iStack_40,iStack_44) /
                  (double)CONCAT44(DAT_00799adc,DAT_00799ad8);
      _DAT_00799ae8 = uStack_24;
      _DAT_00799aec = iStack_20;
      fStack_48 = (float)dStack_1c;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 5) {
      iStack_50 = uStack_24 - DAT_00799af0;
      iStack_4c = (iStack_20 - DAT_00799af4) - (uint)(uStack_24 < DAT_00799af0);
      fVar4 = (float10)CONCAT44(iStack_4c,iStack_50) / (float10)CONCAT44(DAT_00799adc,DAT_00799ad8);
      dStack_2c = (double)fVar4;
      fStack_54 = (float)fVar4;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 0) {
      DAT_00799af0 = uStack_24;
      DAT_00799af4 = iStack_20;
      _DAT_00799ae8 = uStack_24;
      _DAT_00799aec = iStack_20;
      DAT_005ff530 = 0;
      lVar5 = 0;
    }
    else if (param_1 == 1) {
      if (DAT_005ff530 != 0) {
        bVar3 = CARRY4(DAT_00799af0,uStack_24 - DAT_00799ae0);
        DAT_00799af0 = DAT_00799af0 + (uStack_24 - DAT_00799ae0);
        DAT_00799af4 = DAT_00799af4 +
                       ((iStack_20 - DAT_00799ae4) - (uint)(uStack_24 < DAT_00799ae0)) + (uint)bVar3
        ;
      }
      _DAT_00799ae8 = uStack_24;
      _DAT_00799aec = iStack_20;
      DAT_005ff530 = 0;
      lVar5 = 0;
    }
    else if (param_1 == 2) {
      _DAT_00799ae8 = uStack_24;
      _DAT_00799aec = iStack_20;
      DAT_005ff530 = 1;
      lVar5 = CONCAT44(iStack_20,uStack_24);
    }
    else if (param_1 == 3) {
      lVar5 = func_0x0056dcf0(DAT_00799ad8,DAT_00799adc,10,0);
      lVar5 = lVar5 + CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
    else if (param_1 == 4) {
      fVar4 = (float10)CONCAT44(iStack_20,uStack_24) / (float10)CONCAT44(DAT_00799adc,DAT_00799ad8);
      dStack_14 = (double)fVar4;
      fStack_58 = (float)fVar4;
      lVar5 = CONCAT44(DAT_00799ae4,DAT_00799ae0);
    }
  }
  DAT_00799ae4 = (int)((ulonglong)lVar5 >> 0x20);
  DAT_00799ae0 = (uint)lVar5;
  puStack_8 = &UNK_00417527;
  __chkesp();
  return;
}

