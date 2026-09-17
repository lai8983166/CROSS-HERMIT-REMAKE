
void FUN__text__004298e0(char *param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  char *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = local_c & 0xffffff00;
  for (local_8 = param_1; *local_8 != '\0'; local_8 = local_8 + 1) {
    iVar2 = FUN__text__00429820(CONCAT31((int3)((uint)local_8 >> 8),*local_8));
    if (iVar2 == 0) {
      if (((local_c & 0xff) == 0x5c) && (*local_8 == '\\')) break;
      cVar1 = *local_8;
    }
    else {
      cVar1 = *local_8;
      local_8 = local_8 + 1;
    }
    local_c = CONCAT31(local_c._1_3_,cVar1);
  }
  local_8 = (char *)0x42997f;
  FUN__text__0056ce80();
  return;
}

