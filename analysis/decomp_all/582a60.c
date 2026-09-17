
undefined4 FUN__text__00582a60(void)

{
  int iVar1;
  undefined4 local_9c;
  undefined4 local_98 [4];
  int local_88;
  
  local_98[0] = 0x94;
  iVar1 = (*API_KERNEL32_DLL_GetVersionExA)(local_98);
  if ((iVar1 == 0) || (local_88 != 2)) {
    local_9c = 0;
  }
  else {
    local_9c = 1;
  }
  return local_9c;
}

