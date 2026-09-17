
void __fastcall FUN__text__0041ab60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  char *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  do {
    if (local_10 == 0x10) {
LAB__text__0041abd7:
      local_8 = 0x41abe4;
      FUN__text__0056ce80();
      return;
    }
    local_c = (char *)(param_1 + 0x1780 + local_10 * 0x88);
    if (*local_c == '\0') {
      local_8 = param_1;
      _memset(local_c,0,0x88);
      *local_c = '\x01';
      goto LAB__text__0041abd7;
    }
    local_10 = local_10 + 1;
  } while( true );
}

