
/* Library Function - Single Match
    __set_osfhnd
   
   Library: Visual Studio 2003 Debug */

int __cdecl __set_osfhnd(int param_1,intptr_t param_2)

{
  int iVar1;
  undefined4 *puVar2;
  
  if (((uint)param_1 < DAT_0080a900) &&
     (*(int *)((&DAT_0080a800)[param_1 >> 5] + (param_1 & 0x1fU) * 0x24) == -1)) {
    if (DAT_007619fc == 1) {
      if (param_1 == 0) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff6,param_2);
      }
      else if (param_1 == 1) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff5,param_2);
      }
      else if (param_1 == 2) {
        (*API_KERNEL32_DLL_SetStdHandle)(0xfffffff4,param_2);
      }
    }
    *(intptr_t *)((&DAT_0080a800)[param_1 >> 5] + (param_1 & 0x1fU) * 0x24) = param_2;
    iVar1 = 0;
  }
  else {
    puVar2 = (undefined4 *)FUN__text__00576d20();
    *puVar2 = 9;
    puVar2 = (undefined4 *)FUN__text__00576d30();
    *puVar2 = 0;
    iVar1 = -1;
  }
  return iVar1;
}

