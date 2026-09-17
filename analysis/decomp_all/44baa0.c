
void __fastcall FUN__text__0044baa0(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 4; local_c = local_c + 1) {
    if (*(char *)(local_8 + local_c + 0x1a8c) == '\x04') {
      uVar1 = _rand();
      uVar1 = uVar1 & 0x80000003;
      if ((int)uVar1 < 0) {
        uVar1 = (uVar1 - 1 | 0xfffffffc) + 1;
      }
      *(char *)(local_8 + local_c + 0x1a8c) = (char)uVar1;
    }
  }
  local_8 = 0x44bb13;
  FUN__text__0056ce80();
  return;
}

