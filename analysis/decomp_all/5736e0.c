
/* Library Function - Single Match
    __CrtSetReportFile
   
   Library: Visual Studio 2003 Debug */

undefined4 __CrtSetReportFile(int param_1,int param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  if ((param_1 < 0) || (2 < param_1)) {
    uVar1 = 0xfffffffe;
  }
  else if (param_2 == -6) {
    uVar1 = *(undefined4 *)(&DAT_00761b80 + param_1 * 4);
  }
  else {
    uVar1 = *(undefined4 *)(&DAT_00761b80 + param_1 * 4);
    if (param_2 == -4) {
      uVar2 = (*API_KERNEL32_DLL_GetStdHandle)(0xfffffff5);
      *(undefined4 *)(&DAT_00761b80 + param_1 * 4) = uVar2;
    }
    else if (param_2 == -5) {
      uVar2 = (*API_KERNEL32_DLL_GetStdHandle)(0xfffffff4);
      *(undefined4 *)(&DAT_00761b80 + param_1 * 4) = uVar2;
    }
    else {
      *(int *)(&DAT_00761b80 + param_1 * 4) = param_2;
    }
  }
  return uVar1;
}

