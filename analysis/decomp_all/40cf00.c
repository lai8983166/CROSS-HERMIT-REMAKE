
void __thiscall FUN__text__0040cf00(int param_1,int *param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_258 [16];
  undefined4 local_218;
  undefined1 local_214 [520];
  int local_c;
  int local_8;
  
  puVar3 = local_258;
  for (iVar2 = 0x95; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_218 = 0;
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    if ((*param_2 != 0) &&
       (iVar2 = FUN__text__00424f80("seg->g_pSeg == 0",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff138 + 9,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    _memset(local_214,0,0x208);
    (*API_KERNEL32_DLL_MultiByteToWideChar)(0,0,param_3,0xffffffff,local_214,0x104);
    local_c = FUN__text__0056ce80();
    if ((local_c == 0) &&
       (iVar2 = FUN__text__00424f80("ret!=0",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff138 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_c != 0) {
      (**(code **)(**(int **)(local_8 + 0xc) + 0x38))
                (*(undefined4 *)(local_8 + 0xc),&DAT_005cb3dc,&DAT_005caefc,local_214,param_2);
      local_c = FUN__text__0056ce80();
      if (local_c < 0) {
        FUN__text__0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                            DAT_005ff138 + 0x17,local_c,"RegistWaveData()",1);
      }
      else {
        (**(code **)(*(int *)*param_2 + 0x74))(*param_2,*(undefined4 *)(local_8 + 8));
        local_c = FUN__text__0056ce80();
        if (-1 < local_c) goto LAB__text__0040d101;
        FUN__text__0056cbca("E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                            DAT_005ff138 + 0x1d,local_c,"RegistWaveData()",1);
      }
    }
    if ((*param_2 != 0) && (*param_2 != 0)) {
      (**(code **)(*(int *)*param_2 + 8))(*param_2);
      FUN__text__0056ce80();
      *param_2 = 0;
    }
    _memset(param_2,0,0xc);
  }
LAB__text__0040d101:
  local_8 = 0x40d111;
  FUN__text__0056ce80();
  return;
}

