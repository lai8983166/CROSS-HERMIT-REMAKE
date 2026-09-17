
void FUN__text__00442f40(void)

{
  undefined1 uVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_a8 [16];
  undefined4 local_68;
  undefined4 local_64;
  int local_60;
  undefined1 local_5c [13];
  undefined1 local_4f;
  undefined1 local_3a [16];
  undefined2 local_2a [17];
  int local_8;
  
  puVar4 = local_a8;
  for (iVar3 = 0x29; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00419450();
  if (iVar3 == 0) {
    _memset(local_5c,0,0x54);
    local_4f = 0xd;
    local_3a[0] = FUN__text__0044ac50();
    local_2a[0] = FUN__text__0044acd0();
    local_64 = 0x54;
    local_68 = FUN__text__00419f90(local_5c,0x54);
  }
  else {
    _memset(local_5c,0,0x54);
    uVar1 = FUN__text__0044ac50();
    *(undefined1 *)(local_8 + 0x1a95) = uVar1;
    uVar2 = FUN__text__0044acd0();
    *(undefined2 *)(local_8 + 0x1a9a) = uVar2;
    local_4f = 0xd;
    for (local_60 = 0; local_60 != 4; local_60 = local_60 + 1) {
      local_3a[local_60] = *(undefined1 *)(local_8 + local_60 + 0x1a95);
      local_2a[local_60] = *(undefined2 *)(local_8 + 0x1a9a + local_60 * 2);
    }
    local_64 = 0x54;
    local_68 = FUN__text__00419fe0(local_5c,0x54);
  }
  local_8 = 0x44307c;
  FUN__text__0056ce80();
  return;
}

