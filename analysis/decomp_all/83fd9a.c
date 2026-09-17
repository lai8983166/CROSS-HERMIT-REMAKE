
uint FUN__text1__0083fd9a(int param_1,uint param_2)

{
  char *pcVar1;
  char cVar2;
  char cVar3;
  char *pcVar4;
  int iVar5;
  uint uVar6;
  uint local_38;
  uint local_30;
  uint local_1c;
  char *local_18;
  char *local_14;
  uint local_10;
  
  local_30 = *(uint *)(param_1 + 0x74);
  local_18 = (char *)(*(int *)(param_1 + 0x30) + *(int *)(param_1 + 100));
  local_1c = *(uint *)(param_1 + 0x70);
  local_10 = *(uint *)(param_1 + 0x88);
  if (*(int *)(param_1 + 0x24) - 0x106U < *(uint *)(param_1 + 100)) {
    local_38 = *(int *)(param_1 + 100) - (*(int *)(param_1 + 0x24) + -0x106);
  }
  else {
    local_38 = 0;
  }
  pcVar1 = (char *)(*(int *)(param_1 + 0x30) + 0x102 + *(int *)(param_1 + 100));
  cVar2 = local_18[local_1c - 1];
  cVar3 = local_18[local_1c];
  if (*(uint *)(param_1 + 0x84) <= *(uint *)(param_1 + 0x70)) {
    local_30 = local_30 >> 2;
  }
  if (*(uint *)(param_1 + 0x6c) < local_10) {
    local_10 = *(uint *)(param_1 + 0x6c);
  }
  do {
    local_14 = (char *)(*(int *)(param_1 + 0x30) + param_2);
    if ((((local_14[local_1c] == cVar3) && (local_14[local_1c - 1] == cVar2)) &&
        (*local_14 == *local_18)) && (local_14[1] == local_18[1])) {
      local_18 = local_18 + 2;
      local_14 = local_14 + 2;
      while (((((pcVar4 = local_18 + 1, local_18[1] == local_14[1] &&
                (pcVar4 = local_18 + 2, local_18[2] == local_14[2])) &&
               ((pcVar4 = local_18 + 3, local_18[3] == local_14[3] &&
                ((pcVar4 = local_18 + 4, local_18[4] == local_14[4] &&
                 (pcVar4 = local_18 + 5, local_18[5] == local_14[5])))))) &&
              (pcVar4 = local_18 + 6, local_18[6] == local_14[6])) &&
             (pcVar4 = local_18 + 7, local_18[7] == local_14[7]))) {
        local_18 = local_18 + 8;
        local_14 = local_14 + 8;
        pcVar4 = local_18;
        if ((*local_18 != *local_14) || (pcVar1 <= local_18)) break;
      }
      local_18 = pcVar4;
      iVar5 = (int)pcVar1 - (int)local_18;
      uVar6 = -iVar5 + 0x102;
      local_18 = pcVar1 + -0x102;
      if ((int)local_1c < (int)uVar6) {
        *(uint *)(param_1 + 0x68) = param_2;
        local_1c = uVar6;
        if ((int)local_10 <= (int)uVar6) {
LAB__text1__008400af:
          if (*(uint *)(param_1 + 0x6c) < local_1c) {
            local_1c = *(uint *)(param_1 + 0x6c);
          }
          return local_1c;
        }
        cVar2 = local_18[-iVar5 + 0x101];
        cVar3 = local_18[uVar6];
      }
    }
    param_2 = (uint)*(ushort *)
                     (*(int *)(param_1 + 0x38) + (param_2 & *(uint *)(param_1 + 0x2c)) * 2);
    if ((param_2 <= local_38) || (local_30 = local_30 - 1, local_30 == 0))
    goto LAB__text1__008400af;
  } while( true );
}

