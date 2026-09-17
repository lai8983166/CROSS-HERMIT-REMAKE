
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__0084a61b(void)

{
  void *pvVar1;
  char *pcVar2;
  int local_c;
  int local_8;
  
  if (DAT_00876c6c == 0) {
    FUN__text1__0084d023();
  }
  GetModuleFileNameA((HMODULE)0x0,
                     "F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\CROSS HERMIT.EXE",0x104);
  PTR_s_F__project_chaomofa_CROSS_HERMIT_00875684 = s_F__project_chaomofa_CROSS_HERMIT_008756c8;
  pcVar2 = "F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\CROSS HERMIT.EXE";
  if (*DAT_00876c64 != '\0') {
    pcVar2 = DAT_00876c64;
  }
  FUN__text1__0084a6b4(pcVar2,0,0,&local_8,&local_c);
  pvVar1 = _malloc(local_c + local_8 * 4);
  if (pvVar1 == (void *)0x0) {
    __amsg_exit(8);
  }
  FUN__text1__0084a6b4(pcVar2,pvVar1,(void *)((int)pvVar1 + local_8 * 4),&local_8,&local_c);
  _DAT_0087566c = pvVar1;
  _DAT_00875668 = local_8 + -1;
  return;
}

