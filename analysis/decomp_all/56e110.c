
undefined4 FUN__text__0056e110(undefined4 *param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint _Retval;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f94e0;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  ExceptionList = &local_14;
  iVar1 = (*API_KERNEL32_DLL_TlsSetValue)(DAT_00761bc0,param_1);
  if (iVar1 == 0) {
    __amsg_exit(0x10);
  }
  uVar2 = (*API_KERNEL32_DLL_GetCurrentThreadId)();
  *param_1 = uVar2;
  if (PTR_DAT_0076197c != (undefined *)0x0) {
    (*(code *)PTR_DAT_0076197c)();
  }
  local_8 = 0;
  _Retval = (*(code *)param_1[0x12])(param_1[0x13]);
  __endthreadex(_Retval);
  ExceptionList = local_14;
  return 0;
}

