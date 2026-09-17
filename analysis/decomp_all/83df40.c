
undefined4 FUN__text1__0083df40(HWND param_1,int param_2)

{
  int iVar1;
  int iVar2;
  
  if (param_2 == 1) {
    iVar1 = GetSystemMetrics(0x4e);
    iVar2 = GetSystemMetrics(0x4f);
    MoveWindow(param_1,iVar1 << 1,iVar2 << 1,0,0,1);
  }
  return 0;
}

