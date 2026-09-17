
bool FUN__text1__00837667(HANDLE param_1)

{
  GetExitCodeProcess(param_1,(LPDWORD)&DAT_008753dc);
  return DAT_008753dc == 0x103;
}

