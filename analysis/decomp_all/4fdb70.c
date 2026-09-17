
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004fdb70(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0xea) != '\0') {
    local_c = local_c & 0xffffff00;
    local_8 = param_1;
    if ((*(char *)(param_1 + 0xea) == '\x01') || (*(char *)(param_1 + 0xea) == '\x03')) {
      FUN__text__00505260((int)_DAT_007570f0,(int)_DAT_007570f2,(int)_DAT_007570f4,
                          (int)_DAT_007570f6,*(undefined1 *)(param_1 + 0x102),0x80,0x80,0x80);
    }
    else {
      FUN__text__00504f10((int)_DAT_007570f0,(int)_DAT_007570f2,(int)_DAT_007570f4,
                          (int)_DAT_007570f6);
    }
  }
  local_8 = 0x4fdc9c;
  FUN__text__0056ce80();
  return;
}

