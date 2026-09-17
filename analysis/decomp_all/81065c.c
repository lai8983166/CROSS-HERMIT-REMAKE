
uint __thiscall FUN__text1__0081065c(int param_1,char param_2)

{
  byte bVar1;
  byte bVar2;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = 0;
  for (local_c = 1 << (param_2 - 1U & 0x1f); local_c != 0; local_c = local_c >> 1) {
    bVar1 = **(byte **)(param_1 + 0xc);
    bVar2 = *(byte *)(param_1 + 0x14);
    *(byte *)(param_1 + 0x14) = *(byte *)(param_1 + 0x14) >> 1;
    if (*(char *)(param_1 + 0x14) == '\0') {
      *(int *)(param_1 + 0xc) = *(int *)(param_1 + 0xc) + 1;
      if (*(uint *)(param_1 + 0x10) <= *(uint *)(param_1 + 0xc)) {
        *(undefined1 *)(param_1 + 0x15) = 1;
      }
      *(undefined1 *)(param_1 + 0x14) = 0x80;
    }
    if ((bVar1 & bVar2) != 0) {
      local_8 = local_8 | local_c;
    }
  }
  return local_8;
}

