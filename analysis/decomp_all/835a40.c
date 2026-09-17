
HWND FUN__text1__00835a40(int param_1)

{
  LPCDLGTEMPLATEA lpTemplate;
  HWND local_10;
  
  lpTemplate = (LPCDLGTEMPLATEA)FUN__text1__00835b18(param_1);
  local_10 = (HWND)0x0;
  if (param_1 == 0) {
    local_10 = CreateDialogIndirectParamA
                         ((HINSTANCE)PTR_IMAGE_DOS_HEADER_008751e8,lpTemplate,(HWND)0x0,
                          FUN__text1__00835ac5,0);
    GetLastError();
  }
  FUN__text1__00848476(lpTemplate);
  ShowWindow(local_10,5);
  UpdateWindow(local_10);
  return local_10;
}

