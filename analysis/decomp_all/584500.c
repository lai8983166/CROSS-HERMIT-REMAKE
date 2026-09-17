
void FUN__text__00584500(void)

{
  int iVar1;
  int *piVar2;
  
  piVar2 = (int *)FUN__text__00584380();
  iVar1 = *piVar2;
  __setdefaultprecision();
  if ((iVar1 != 0) && ((**(uint **)(iVar1 + 4) & 0x10008) != 0)) {
    iVar1 = *(int *)(iVar1 + 4);
    *(undefined4 *)(iVar1 + 0x20) = 0;
    *(undefined4 *)(iVar1 + 0x24) = 0xffff;
  }
  return;
}

