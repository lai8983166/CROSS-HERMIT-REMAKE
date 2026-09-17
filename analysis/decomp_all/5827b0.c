
void FUN__text__005827b0(void)

{
  size_t sVar1;
  
  sVar1 = _strlen(DAT_0080a67c);
  DAT_0080a66c = (uint)(sVar1 == 3);
  (*API_KERNEL32_DLL_EnumSystemLocalesA)(FUN__text__00582800,1);
  if ((DAT_0080a680 & 4) == 0) {
    DAT_0080a680 = 0;
  }
  return;
}

