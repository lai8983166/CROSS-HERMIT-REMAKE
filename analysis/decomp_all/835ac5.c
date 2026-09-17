
undefined4 FUN__text1__00835ac5(HWND param_1,int param_2)

{
  HWND hWnd;
  char *lpString;
  
  if (param_2 == 0x110) {
    SetWindowTextA(param_1,"");
    lpString = "Loading...";
    hWnd = GetDlgItem(param_1,0x3ea);
    SetWindowTextA(hWnd,lpString);
  }
  return 0;
}

