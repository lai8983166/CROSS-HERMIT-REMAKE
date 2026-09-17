
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0057ce80(void)

{
  char *local_18;
  int local_10;
  int local_c;
  int local_8;
  
  if (DAT_0080bb80 == 0) {
    FUN__text__0057c3f0();
  }
  (*API_KERNEL32_DLL_GetModuleFileNameA)
            (0,"F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\CROSS HERMIT.EXE",0x104);
  PTR_s_F__project_chaomofa_CROSS_HERMIT_0080a418 = s_F__project_chaomofa_CROSS_HERMIT_0080a4fc;
  if (*DAT_0080bb74 == '\0') {
    local_18 = "F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\CROSS HERMIT.EXE";
  }
  else {
    local_18 = DAT_0080bb74;
  }
  FUN__text__0057cf60(local_18,0,0,&local_10,&local_8);
  local_c = __malloc_dbg(local_8 + local_10 * 4,2,"stdargv.c",0x80);
  if (local_c == 0) {
    __amsg_exit(8);
  }
  FUN__text__0057cf60(local_18,local_c,local_c + local_10 * 4,&local_10,&local_8);
  _DAT_0080a3fc = local_10 + -1;
  _DAT_0080a400 = local_c;
  return;
}

