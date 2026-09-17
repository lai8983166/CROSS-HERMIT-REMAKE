
void FUN__text__00458380(undefined2 param_1,undefined2 param_2,undefined1 param_3,undefined1 param_4
                        )

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  undefined4 local_24;
  undefined1 local_20 [13];
  undefined1 local_13;
  undefined1 local_10;
  undefined1 local_f;
  undefined2 local_e;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if (iVar1 != 0) {
    _memset(local_20,0,0x18);
    local_13 = 0x10;
    local_10 = param_3;
    local_f = param_4;
    local_e = param_1;
    local_c = param_2;
    iVar1 = FUN__text__00419450();
    if (iVar1 == 0) {
      local_24 = FUN__text__00419f90(local_20,0x18);
    }
    else {
      local_24 = FUN__text__00419fe0(local_20,0x18);
    }
  }
  local_8 = 0x458447;
  FUN__text__0056ce80();
  return;
}

