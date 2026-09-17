
void FUN__text__00582610(void)

{
  size_t sVar1;
  undefined4 extraout_var;
  
  sVar1 = _strlen(DAT_0080a678);
  DAT_0080a674 = (uint)(sVar1 == 3);
  if (DAT_0080a674 == 0) {
    DAT_0080a670 = _GetPrimaryLen(DAT_0080a678,extraout_var);
  }
  else {
    DAT_0080a670 = 2;
  }
  (*API_KERNEL32_DLL_EnumSystemLocalesA)(FUN__text__00582690,1);
  if ((DAT_0080a680 & 4) == 0) {
    DAT_0080a680 = 0;
  }
  return;
}

