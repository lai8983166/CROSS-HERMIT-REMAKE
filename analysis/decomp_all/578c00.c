
uint FUN_00578c00(int param_1)

{
  uint local_c;
  
  local_c = DAT_0080ab48;
  while( true ) {
    if (DAT_0080ab48 + DAT_0080ab44 * 0x14 <= local_c) {
      return 0;
    }
    if ((uint)(param_1 - *(int *)(local_c + 0xc)) < 0x100000) break;
    local_c = local_c + 0x14;
  }
  return local_c;
}

