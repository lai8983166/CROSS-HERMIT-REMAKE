
bool FUN__text__0054bd13(int param_1)

{
  int iVar1;
  int iVar2;
  bool bVar3;
  
  iVar1 = param_1;
  bVar3 = true;
  if ((*(byte *)(param_1 + 0x10c) & 0x20) == 0) {
    if ((*(byte *)(param_1 + 0x5d) & 8) == 0) goto LAB__text__0054bd3f;
  }
  else if ((*(uint *)(param_1 + 0x5c) & 0x300) != 0x300) goto LAB__text__0054bd3f;
  bVar3 = false;
LAB__text__0054bd3f:
  FUN__text__00546578(param_1,&param_1,4);
  if (bVar3) {
    iVar2 = FUN__text__0054bcc3(&param_1);
    bVar3 = iVar2 != *(int *)(iVar1 + 0x100);
  }
  else {
    bVar3 = false;
  }
  return bVar3;
}

