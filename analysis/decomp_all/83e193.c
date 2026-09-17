
void __thiscall FUN__text1__0083e193(undefined4 param_1,HWND param_2,LPCSTR param_3)

{
  WPARAM wParam;
  int iVar1;
  
  if (DAT_00875438 == '\0') {
    FUN__text1__0083e0c4(param_1);
  }
  if ((DAT_00875435 == '\0') && (DAT_00875434 == '\0')) {
    if (DAT_00875640 == (HWND)0x0) {
      iVar1 = MessageBoxA(param_2,param_3,"",0x10001);
      if (iVar1 == 2) {
                    /* WARNING: Subroutine does not return */
        ExitProcess(1);
      }
    }
    else {
      wParam = SendMessageA(DAT_00875640,0x180,0,(LPARAM)param_3);
      SendMessageA(DAT_00875640,0x186,wParam,0);
      UpdateWindow(DAT_00875640);
    }
  }
  return;
}

