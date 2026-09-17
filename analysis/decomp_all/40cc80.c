
void __thiscall FUN__text__0040cc80(int param_1,int *param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_3ac [16];
  undefined4 local_36c;
  int local_368;
  int local_364;
  undefined4 local_360;
  undefined4 local_35c;
  undefined4 local_348;
  undefined4 local_344;
  undefined4 local_340;
  undefined4 local_33c;
  int local_20;
  undefined4 local_1c;
  int local_18;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_3ac;
  for (iVar2 = 0xea; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_36c = 0;
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    if ((*param_2 != 0) &&
       (iVar2 = FUN__text__00424f80("seg->g_pSeg == 0",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff134 + 0xc,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    iVar2 = FUN__text__0040c0f0(param_3);
    if (iVar2 == 0) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                  DAT_005ff134 + 0xf,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    else {
      local_368 = param_3;
      local_10 = *(int *)(param_3 + 4) + 8;
      local_c = 0;
      _memset(&local_360,0,0x350);
      local_360 = 0x350;
      local_348 = DAT_005cb3dc;
      local_344 = DAT_005cb3e0;
      local_340 = DAT_005cb3e4;
      local_33c = DAT_005cb3e8;
      local_35c = 0x402;
      local_18 = param_3;
      local_20 = local_10;
      local_1c = local_c;
      (**(code **)(**(int **)(local_8 + 0xc) + 0xc))
                (*(undefined4 *)(local_8 + 0xc),&local_360,&DAT_005caefc,param_2);
      local_364 = FUN__text__0056ce80();
      if (local_364 < 0) {
        FUN__text__0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                            DAT_005ff134 + 0x44,local_364,"RegistWaveData()",1);
      }
      else {
        (**(code **)(*(int *)*param_2 + 0x74))(*param_2,*(undefined4 *)(local_8 + 8));
        local_364 = FUN__text__0056ce80();
        if (-1 < local_364) goto LAB__text__0040cee8;
        FUN__text__0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                            DAT_005ff134 + 0x52,local_364,"RegistWaveData()",1);
      }
      if ((*param_2 != 0) && (*param_2 != 0)) {
        (**(code **)(*(int *)*param_2 + 8))(*param_2);
        FUN__text__0056ce80();
        *param_2 = 0;
      }
      _memset(param_2,0,0xc);
    }
  }
LAB__text__0040cee8:
  local_8 = 0x40cef8;
  FUN__text__0056ce80();
  return;
}

