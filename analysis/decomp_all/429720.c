
void FUN__text__00429720(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [14];
  undefined4 uStack_10;
  uint local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset("F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\",0x20d,0);
  (*API_KERNEL32_DLL_GetCurrentDirectoryA)
            (0x20d,"F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\");
  local_8 = FUN__text__0056ce80();
  if (local_8 < 0x20e) {
    FUN__text__004297a0("F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\");
  }
  uStack_10 = 0x429794;
  FUN__text__0056ce80();
  return;
}

