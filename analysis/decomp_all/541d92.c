
uint FUN__text__00541d92(int param_1)

{
  uint uVar1;
  int iVar2;
  uint *puVar3;
  uint local_9c [3];
  ushort local_90;
  int local_8c;
  char local_5;
  
  puVar3 = local_9c;
  for (iVar2 = 0x25; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  }
  local_5 = '\0';
  local_9c[0] = 0x94;
  iVar2 = (*API_KERNEL32_DLL_GetVersionExA)(local_9c);
  if (iVar2 == 0) {
    local_5 = '\x01';
  }
  if (local_8c == 1) {
    if ((local_9c[1] < 5) && (((local_9c[1] != 4 || (local_9c[2] < 10)) || (local_90 < 0x55d)))) {
      local_5 = '\x01';
    }
  }
  else {
    if (local_8c != 2) {
      return 0;
    }
    if (iVar2 != 0) {
      if (param_1 != 10) {
        uVar1 = (*API_KERNEL32_DLL_IsProcessorFeaturePresent)(param_1);
        return uVar1;
      }
      goto LAB__text__00541e37;
    }
  }
  if (param_1 == 6) {
    if (local_5 == '\0') {
      uVar1 = FUN__text__00541ced();
      return uVar1 & 4;
    }
  }
  else {
    if (param_1 == 7) {
      uVar1 = FUN__text__00541cb5();
      return uVar1;
    }
    if ((param_1 == 10) && (local_5 == '\0')) {
LAB__text__00541e37:
      uVar1 = FUN__text__00541ced();
      return uVar1 & 8;
    }
  }
  return 0;
}

