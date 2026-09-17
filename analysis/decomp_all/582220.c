
void FUN__text__00582220(void)

{
  size_t sVar1;
  undefined4 extraout_var;
  undefined4 uVar2;
  
  sVar1 = _strlen(DAT_0080a678);
  DAT_0080a674 = (uint)(sVar1 == 3);
  uVar2 = extraout_var;
  sVar1 = _strlen(DAT_0080a67c);
  DAT_0080a66c = (uint)(sVar1 == 3);
  DAT_0080a668 = 0;
  if (DAT_0080a674 == 0) {
    DAT_0080a670 = _GetPrimaryLen(DAT_0080a678,uVar2);
  }
  else {
    DAT_0080a670 = 2;
  }
  (*API_KERNEL32_DLL_EnumSystemLocalesA)(FUN__text__005822e0,1);
  if ((((DAT_0080a680 & 0x100) == 0) || ((DAT_0080a680 & 0x200) == 0)) || ((DAT_0080a680 & 7) == 0))
  {
    DAT_0080a680 = 0;
  }
  return;
}

