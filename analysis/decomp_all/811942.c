
uint FUN__text1__00811942(uint param_1,uint param_2)

{
  int iVar1;
  int *piVar2;
  uint local_14;
  uint local_c;
  
  local_c = param_2 << 7 ^ param_1;
  if (local_c == 0) {
    local_14 = 1;
  }
  else {
    local_14 = 0x88cf - local_c;
  }
  while ((piVar2 = (int *)(DAT_00874448 + local_c * 0xc), *piVar2 != -1 &&
         ((piVar2[1] != param_1 || (*(byte *)(piVar2 + 2) != param_2))))) {
    if (local_c < local_14) {
      iVar1 = 0x88cf - local_14;
    }
    else {
      iVar1 = -local_14;
    }
    local_c = local_c + iVar1;
  }
  return local_c;
}

