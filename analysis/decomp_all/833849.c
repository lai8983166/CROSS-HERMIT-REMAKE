
bool FUN__text1__00833849(HWND param_1)

{
  char cVar1;
  ATOM AVar2;
  ATOM AVar3;
  DWORD local_8;
  
  GetWindowThreadProcessId(param_1,&local_8);
  if ((local_8 == DAT_00874868) && (param_1 != DAT_00874840)) {
    cVar1 = FUN__text1__0083309d();
    if (cVar1 == '\0') {
      AVar2 = GlobalAddAtomA("");
      AVar3 = GlobalAddAtomA("System");
      SendMessageA(param_1,0x3e0,(WPARAM)DAT_00874840,CONCAT22(AVar3,AVar2));
    }
    else {
      AVar2 = GlobalAddAtomW(L"CROSS HERMIT");
      AVar3 = GlobalAddAtomW(L"System");
      SendMessageW(param_1,0x3e0,(WPARAM)DAT_00874840,CONCAT22(AVar3,AVar2));
    }
  }
  return DAT_00874844 == 0;
}

