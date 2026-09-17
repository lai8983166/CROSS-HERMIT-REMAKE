
undefined4 __fastcall FUN__text__00548706(int param_1)

{
  int iVar1;
  
  if (*(int *)(param_1 + 0x6c) != 0) {
    iVar1 = *(int *)(param_1 + 0xa8);
    if (iVar1 != 0) {
      (*API_GDI32_DLL_SelectObject)(*(int *)(param_1 + 0x6c),iVar1);
      *(int *)(param_1 + 0xa8) = 0;
    }
  }
  return 0;
}

