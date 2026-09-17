
int FUN__text1__008104b9(int param_1,int param_2)

{
  byte bVar1;
  byte bVar2;
  undefined4 local_c;
  undefined4 local_8;
  
  for (local_c = 0; *(int *)(param_1 + 0x414 + local_c * 0x10) == 0;
      local_c = local_c + (uint)((bVar1 & bVar2) != 0)) {
    local_c = *(int *)(param_1 + 0x418 + local_c * 0x10);
    bVar1 = **(byte **)(param_2 + 0xc);
    bVar2 = *(byte *)(param_2 + 0x14);
    *(byte *)(param_2 + 0x14) = *(byte *)(param_2 + 0x14) >> 1;
    if (*(char *)(param_2 + 0x14) == '\0') {
      *(int *)(param_2 + 0xc) = *(int *)(param_2 + 0xc) + 1;
      if (*(uint *)(param_2 + 0x10) <= *(uint *)(param_2 + 0xc)) {
        *(undefined1 *)(param_2 + 0x15) = 1;
      }
      *(undefined1 *)(param_2 + 0x14) = 0x80;
    }
  }
  local_8 = *(int *)(param_1 + 0x418 + local_c * 0x10);
  if (local_8 == 0x101) {
    local_8 = FUN__text1__0081065c(8);
    FUN__text1__0081029b(param_1,local_8);
  }
  return local_8;
}

