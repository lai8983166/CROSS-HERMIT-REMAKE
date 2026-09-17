
void FUN__text1__0083dc8f(undefined4 *param_1,DWORD param_2)

{
  char cVar1;
  BOOL BVar2;
  CONTEXT local_2d0;
  
  do {
    cVar1 = FUN__text1__00837667(*param_1);
    if (cVar1 == '\0') {
      return;
    }
    ResumeThread((HANDLE)param_1[1]);
    Sleep(100);
    SuspendThread((HANDLE)param_1[1]);
    _memset(&local_2d0,0,0x2cc);
    local_2d0.ContextFlags = 0x10001;
    BVar2 = GetThreadContext((HANDLE)param_1[1],&local_2d0);
  } while ((BVar2 == 0) || (local_2d0.Eip != param_2));
  return;
}

