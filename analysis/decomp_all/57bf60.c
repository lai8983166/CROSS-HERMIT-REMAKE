
/* Library Function - Single Match
    _getSystemCP
   
   Library: Visual Studio 2003 Debug */

int __cdecl getSystemCP(int param_1)

{
  DAT_0080a4f8 = 0;
  if (param_1 == -2) {
    DAT_0080a4f8 = 1;
    param_1 = (*API_KERNEL32_DLL_GetOEMCP)();
  }
  else if (param_1 == -3) {
    DAT_0080a4f8 = 1;
    param_1 = (*DAT_00592124)();
  }
  else if (param_1 == -4) {
    DAT_0080a4f8 = 1;
    param_1 = DAT_0080a63c;
  }
  return param_1;
}

