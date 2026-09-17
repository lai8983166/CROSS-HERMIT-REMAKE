
bool FUN__text1__00837ca0(HWND param_1)

{
  LRESULT LVar1;
  
  LVar1 = SendMessageA(param_1,0x11,0,0);
  if (LVar1 == 0) {
    SetPropA(param_1,"Shutdown",(HANDLE)0x0);
  }
  return LVar1 != 0;
}

