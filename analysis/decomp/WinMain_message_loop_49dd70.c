
void WinMain_message_loop
               (undefined *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_a0 [16];
  undefined4 uStack_60;
  int iStack_5c;
  int iStack_58;
  int iStack_54;
  int iStack_50;
  int iStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  int iStack_3c;
  undefined4 uStack_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined1 auStack_24 [28];
  undefined *puStack_8;
  
  puVar3 = auStack_a0;
  for (iVar2 = 0x27; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  puStack_8 = (undefined *)0x0;
  uVar1 = func_0x00571020(0);
  func_0x00570fd0(uVar1);
  FUN_0042b2d0("GAME_WORK_SYSTEM = %08x\n",0x11730);
  FUN_0042b2d0("ANIM_WORK = %08x\n",0x58);
  func_0x004288e0();
  iStack_50 = func_0x00428a40(0x1110);
  if (iStack_50 == 0) {
    iStack_5c = 0;
  }
  else {
    iStack_5c = func_0x0044fbb0();
  }
  iStack_4c = iStack_5c;
  DAT_007a4a00 = iStack_5c;
  if (iStack_5c != 0) {
    func_0x00421660();
    PTR_IMAGE_DOS_HEADER_007a2728 = param_1;
    (*API_KERNEL32_DLL_lstrcpyA)("Cross Hermit","Cross Hermit");
    __chkesp();
    iVar2 = func_0x004293e0();
    if (iVar2 == 0) {
      func_0x00450290(param_3);
      *(undefined4 *)(DAT_007a4a00 + 0x5c) = 0x69;
      *(undefined4 *)(DAT_007a4a00 + 0x60) = 0x67;
      uStack_28 = 0;
      uStack_2c = 0;
      uStack_30 = 0x400;
      uStack_34 = 0x300;
      uStack_38 = 0x90000000;
      iVar2 = create_window_2(0,0,0x400,0x300,0x90000000,param_4);
      if (iVar2 == 0) {
        (*API_OLE32_DLL_CoInitialize)(0);
        iStack_3c = __chkesp();
        if (iStack_3c < 0) {
          (*DAT_005923d8)(PTR_DAT_007a0bb4,&DAT_005a074c,"Cross Hermit",0x10);
          __chkesp();
          (*API_USER32_DLL_DestroyWindow)(PTR_DAT_007a0bb4);
          __chkesp();
        }
        else {
          uStack_44 = 8;
          uStack_40 = 0x800;
          (*API_COMCTL32_DLL_InitCommonControlsEx)(&uStack_44);
          uStack_48 = __chkesp();
          iVar2 = func_0x00450570(PTR_DAT_007a0bb4,&DAT_007a49fc,uStack_30,uStack_34);
          if (iVar2 == 0) {
            (*API_USER32_DLL_InvalidateRect)(PTR_DAT_007a0bb4,0,1);
            __chkesp();
            func_0x0042b240(0);
            func_0x0049e1b0();
            while( true ) {
              while( true ) {
                (*API_USER32_DLL_PeekMessageA)(auStack_24,0,0,0,0);
                iVar2 = __chkesp();
                if (iVar2 != 0) break;
                if (*(int *)(DAT_007a4a00 + 0x8d0) == 0) {
                  (*API_USER32_DLL_WaitMessage)();
                  __chkesp();
                }
                else {
                  game_tick_frame();
                  if (*(int *)(DAT_007a4a00 + 0x8e0) == 1) {
                    (*API_USER32_DLL_DestroyWindow)(PTR_DAT_007a0bb4);
                    __chkesp();
                  }
                }
              }
              (*API_USER32_DLL_GetMessageA)(auStack_24,0,0,0);
              iVar2 = __chkesp();
              if (iVar2 == 0) break;
              (*API_USER32_DLL_TranslateMessage)(auStack_24);
              __chkesp();
              (*API_USER32_DLL_DispatchMessageA)(auStack_24);
              __chkesp();
            }
          }
          else {
            (*API_USER32_DLL_DestroyWindow)(PTR_DAT_007a0bb4);
            __chkesp();
          }
        }
      }
      else {
        (*DAT_005923d8)(0,&DAT_005a075c,"Cross Hermit",0x10);
        __chkesp();
      }
    }
  }
  if (DAT_007a4a00 != 0) {
    FUN_00421bf0();
    if (DAT_007a49fc != 0) {
      func_0x00416870();
      FUN_00417cc0();
    }
    func_0x00450730(&DAT_007a49fc);
    iStack_58 = DAT_007a4a00;
    iStack_54 = DAT_007a4a00;
    if (DAT_007a4a00 == 0) {
      uStack_60 = 0;
    }
    else {
      uStack_60 = func_0x0049e150(1);
    }
    DAT_007a4a00 = 0;
  }
  func_0x0042b240(1);
  (*API_COMBASE_DLL_CoUninitialize)();
  __chkesp();
  func_0x00428910();
  puStack_8 = &UNK_0049e144;
  __chkesp();
  return;
}

