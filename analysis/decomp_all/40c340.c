
void __thiscall FUN__text__0040c340(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_464 [16];
  undefined1 local_424 [260];
  undefined1 local_320 [520];
  undefined1 local_118 [252];
  undefined4 uStack_1c;
  int local_14;
  undefined *local_10;
  undefined2 local_c;
  int local_8;
  
  puVar3 = local_464;
  for (iVar2 = 0x118; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = PTR_s___005bfff4_0x3a_00592ad0;
  local_c = DAT_00592ad4;
  local_8 = param_1;
  (*API_COMBASE_DLL_CoCreateInstance)(&DAT_005cb3ec,0,3,&DAT_005caf0c,param_1 + 8);
  local_14 = FUN__text__0056ce80();
  if (local_14 < 0) {
    FUN__text__0042b2d0("DxAudio Err:CoCreateInstance(CLSID_DirectMusicPerformance)\n");
  }
  else {
    (**(code **)(**(int **)(local_8 + 8) + 0xb0))
              (*(undefined4 *)(local_8 + 8),0,0,PTR_DAT_007a0bb4,8,0x40,0x3f,0);
    local_14 = FUN__text__0056ce80();
    if (local_14 < 0) {
      FUN__text__0042b2d0("DxAudio Err:InitAudio()\n");
    }
    else {
      (**(code **)(**(int **)(local_8 + 8) + 0xcc))(*(undefined4 *)(local_8 + 8),local_8 + 0x10);
      local_14 = FUN__text__0056ce80();
      if (local_14 < 0) {
        FUN__text__0042b2d0("DxAudio Err:GetDefaultAudioPath()\n");
      }
      else {
        (*API_COMBASE_DLL_CoCreateInstance)(&DAT_005cb37c,0,3,&DAT_005caf1c,local_8 + 0xc);
        local_14 = FUN__text__0056ce80();
        if (local_14 < 0) {
          FUN__text__0042b2d0("DxAudio Err:CoCreateInstance(CLSID_DirectMusicLoader)\n");
        }
        else {
          FUN__text__0056d810(local_118,&DAT_00592a18,param_2);
          FUN__text__004297a0(local_118);
          _memset(local_320,0,0x208);
          (*API_KERNEL32_DLL_MultiByteToWideChar)(0,0,local_118,0xffffffff,local_320,0x104);
          local_14 = FUN__text__0056ce80();
          if ((local_14 == 0) &&
             (iVar2 = FUN__text__00424f80("ret!=0",
                                          "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP"
                                          ,DAT_005ff124 + 0x2d,0), iVar2 != 0)) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          _memset(local_424,0,0x104);
          (*API_KERNEL32_DLL_WideCharToMultiByte)(0,0,local_320,0xffffffff,local_424,0x104,0,0);
          local_14 = FUN__text__0056ce80();
          if ((local_14 == 0) &&
             (iVar2 = FUN__text__00424f80("ret!=0",
                                          "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP"
                                          ,DAT_005ff124 + 0x32,0), iVar2 != 0)) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          (**(code **)(**(int **)(local_8 + 0xc) + 0x14))
                    (*(undefined4 *)(local_8 + 0xc),&DAT_005cb2fc,&local_10,0);
          local_14 = FUN__text__0056ce80();
          if (-1 < local_14) {
            FUN__text__0040d6c0(*(undefined4 *)(local_8 + 4));
            goto LAB__text__0040c5ee;
          }
        }
      }
    }
  }
  FUN__text__0042b2d0("DxAudio Err:ret = %08x\n",local_14);
  FUN__text__0040bfa0();
LAB__text__0040c5ee:
  uStack_1c = 0x40c5fe;
  FUN__text__0056ce80();
  return;
}

