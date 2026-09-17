
void FUN__text__0057cd30(void)

{
  size_t sVar1;
  int iVar2;
  int *local_10;
  int local_c;
  char *local_8;
  
  if (DAT_0080bb80 == 0) {
    FUN__text__0057c3f0();
  }
  local_c = 0;
  for (local_8 = DAT_0080a460; *local_8 != '\0'; local_8 = local_8 + sVar1 + 1) {
    if (*local_8 != '=') {
      local_c = local_c + 1;
    }
    sVar1 = _strlen(local_8);
  }
  local_10 = (int *)__malloc_dbg(local_c * 4 + 4,2,"stdenvp.c",0x6d);
  DAT_0080a408 = local_10;
  if (local_10 == (int *)0x0) {
    __amsg_exit(9);
  }
  for (local_8 = DAT_0080a460; *local_8 != '\0'; local_8 = local_8 + sVar1 + 1) {
    sVar1 = _strlen(local_8);
    if (*local_8 != '=') {
      iVar2 = __malloc_dbg(sVar1 + 1,2,"stdenvp.c",0x79);
      *local_10 = iVar2;
      if (*local_10 == 0) {
        __amsg_exit(9);
      }
      FUN__text__0056cd90(*local_10,local_8);
      local_10 = local_10 + 1;
    }
  }
  __free_dbg(DAT_0080a460,2);
  DAT_0080a460 = (char *)0x0;
  *local_10 = 0;
  DAT_0080bb7c = 1;
  return;
}

