
void FUN__text1__0084a562(void)

{
  char cVar1;
  size_t sVar2;
  undefined4 *puVar3;
  void *pvVar4;
  int iVar5;
  char *pcVar6;
  
  if (DAT_00876c6c == 0) {
    FUN__text1__0084d023();
  }
  iVar5 = 0;
  for (pcVar6 = DAT_008756b8; *pcVar6 != '\0'; pcVar6 = pcVar6 + sVar2 + 1) {
    if (*pcVar6 != '=') {
      iVar5 = iVar5 + 1;
    }
    sVar2 = _strlen(pcVar6);
  }
  puVar3 = _malloc(iVar5 * 4 + 4);
  DAT_00875674 = puVar3;
  if (puVar3 == (undefined4 *)0x0) {
    __amsg_exit(9);
  }
  cVar1 = *DAT_008756b8;
  pcVar6 = DAT_008756b8;
  while (cVar1 != '\0') {
    sVar2 = _strlen(pcVar6);
    if (*pcVar6 != '=') {
      pvVar4 = _malloc(sVar2 + 1);
      *puVar3 = pvVar4;
      if (pvVar4 == (void *)0x0) {
        __amsg_exit(9);
      }
      FUN__text1__00848d20(*puVar3,pcVar6);
      puVar3 = puVar3 + 1;
    }
    pcVar6 = pcVar6 + sVar2 + 1;
    cVar1 = *pcVar6;
  }
  FUN__text1__008497d3(DAT_008756b8);
  DAT_008756b8 = (char *)0x0;
  *puVar3 = 0;
  DAT_00876c68 = 1;
  return;
}

