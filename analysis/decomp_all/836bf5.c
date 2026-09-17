
undefined1 FUN__text1__00836bf5(LPCSTR param_1,undefined1 param_2,undefined1 param_3)

{
  HANDLE hFile;
  DWORD nNumberOfBytesToRead;
  void *lpBuffer;
  BOOL BVar1;
  undefined1 local_14;
  DWORD local_8;
  
  local_14 = 0;
  hFile = CreateFileA(param_1,0x80000000,1,(LPSECURITY_ATTRIBUTES)0x0,3,0x8000080,(HANDLE)0x0);
  if (hFile == (HANDLE)0xffffffff) {
    local_14 = 0;
  }
  else {
    nNumberOfBytesToRead = GetFileSize(hFile,(LPDWORD)0x0);
    lpBuffer = operator_new(nNumberOfBytesToRead);
    BVar1 = ReadFile(hFile,lpBuffer,nNumberOfBytesToRead,&local_8,(LPOVERLAPPED)0x0);
    if (BVar1 != 0) {
      local_14 = FUN__text1__00836597(lpBuffer,param_2,param_3);
    }
    FUN__text1__00848476(lpBuffer);
    CloseHandle(hFile);
  }
  return local_14;
}

