
void __fastcall FUN__text__00425de0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  if (*(char *)(param_1 + 0x630) != '\0') {
    local_8 = param_1;
    if (*(char *)(param_1 + 0x630) < '\x01') {
      local_c = FUN__text__00425e60(0);
    }
    else {
      local_c = FUN__text__00425e60(1);
    }
    *(undefined1 *)(local_8 + 0x630) = 0;
  }
  local_8 = 0x425e56;
  FUN__text__0056ce80();
  return;
}

