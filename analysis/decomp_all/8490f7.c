
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__008490f7(UINT param_1,int param_2,int param_3)

{
  HANDLE hProcess;
  undefined4 *puVar1;
  UINT uExitCode;
  
  if (DAT_00875694 == 1) {
    uExitCode = param_1;
    hProcess = GetCurrentProcess();
    TerminateProcess(hProcess,uExitCode);
  }
  _DAT_00875690 = 1;
  DAT_0087568c = (undefined1)param_3;
  if (param_2 == 0) {
    if ((DAT_00876c74 != (undefined4 *)0x0) &&
       (puVar1 = (undefined4 *)(DAT_00876c70 - 4), DAT_00876c74 <= puVar1)) {
      do {
        if ((code *)*puVar1 != (code *)0x0) {
          (*(code *)*puVar1)();
        }
        puVar1 = puVar1 + -1;
      } while (DAT_00876c74 <= puVar1);
    }
    FUN__text1__00849190(&DAT_0086e2ac,&DAT_0086e2b4);
  }
  FUN__text1__00849190(&DAT_0086e2b8,&DAT_0086e2bc);
  if (param_3 != 0) {
    return;
  }
  DAT_00875694 = 1;
                    /* WARNING: Subroutine does not return */
  ExitProcess(param_1);
}

