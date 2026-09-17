
void __thiscall FUN__text__0040a100(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  for (local_c = *(int *)(param_2 + 0x20); local_c != 0; local_c = *(int *)(local_c + 0x20)) {
    *(undefined1 *)(local_c + 1) = 0;
  }
  local_8 = param_1;
  if (*(int *)(param_2 + 4) == 0) {
    local_14 = 1;
  }
  else {
    local_10 = FUN__text__0040a800(param_2);
    if (local_10 != 0) {
      local_14 = 1;
    }
  }
  do {
    local_c = *(int *)(param_2 + 0x20);
    while( true ) {
      if (local_c == 0) {
        local_8 = 0x40a1d6;
        FUN__text__0056ce80();
        return;
      }
      if ((*(char *)(local_c + 1) == '\0') &&
         (local_10 = FUN__text__0040a800(local_c), local_10 != 0)) break;
      local_c = *(int *)(local_c + 0x20);
    }
  } while( true );
}

