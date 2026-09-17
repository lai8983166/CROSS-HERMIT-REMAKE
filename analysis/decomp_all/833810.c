
LPCWSTR FUN__text1__00833810(LPCWSTR param_1,LPCWSTR param_2,int param_3)

{
  BOOL BVar1;
  
  BVar1 = IsBadReadPtr(param_1,1);
  if (BVar1 == 0) {
    WideCharToMultiByte(0,0,param_1,-1,(LPSTR)param_2,param_3,(LPCSTR)0x0,(LPBOOL)0x0);
    param_1 = param_2;
  }
  return param_1;
}

