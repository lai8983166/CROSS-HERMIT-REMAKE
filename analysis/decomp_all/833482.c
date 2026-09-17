
undefined4 FUN__text1__00833482(void)

{
  HANDLE hObject;
  BOOL BVar1;
  undefined4 uVar2;
  DWORD local_8;
  
  hObject = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,FUN__text1__008334df,(LPVOID)0x0,0,&local_8);
  CloseHandle(hObject);
  if (hObject == (HANDLE)0x0) {
    uVar2 = 0;
  }
  else {
    while( true ) {
      BVar1 = IsWindow(DAT_00874840);
      if (BVar1 != 0) break;
      Sleep(1);
    }
    Sleep(100);
    uVar2 = 1;
  }
  return uVar2;
}

