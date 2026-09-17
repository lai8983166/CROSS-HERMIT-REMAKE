
void __fastcall FUN__text__0053fa49(char *param_1)

{
  byte bVar1;
  char cVar2;
  int iVar3;
  char *pcVar4;
  uint uVar5;
  byte *pbVar6;
  byte *pbVar7;
  char *pcVar8;
  char **ppcVar9;
  bool bVar10;
  char *local_c [2];
  
  *(undefined4 *)(param_1 + 0x3dc) = *(undefined4 *)(param_1 + 0x1d0);
  if (*(int *)(param_1 + 0xb0) == 0) {
    *(undefined4 *)(param_1 + 0x2d4) = *(undefined4 *)(param_1 + 0x1d0);
  }
  else {
    pbVar7 = (byte *)(param_1 + 0x1d4);
    pbVar6 = (byte *)(param_1 + 0x2d8);
    do {
      bVar1 = *pbVar6;
      bVar10 = bVar1 < *pbVar7;
      if (bVar1 != *pbVar7) {
LAB__text__0053faa1:
        iVar3 = (1 - (uint)bVar10) - (uint)(bVar10 != 0);
        goto LAB__text__0053faa6;
      }
      if (bVar1 == 0) break;
      bVar1 = pbVar6[1];
      bVar10 = bVar1 < pbVar7[1];
      if (bVar1 != pbVar7[1]) goto LAB__text__0053faa1;
      pbVar6 = pbVar6 + 2;
      pbVar7 = pbVar7 + 2;
    } while (bVar1 != 0);
    iVar3 = 0;
LAB__text__0053faa6:
    local_c[0] = param_1;
    local_c[1] = param_1;
    if (iVar3 != 0) {
      local_c[1] = param_1 + 0x1d4;
      pcVar4 = local_c[1];
      do {
        cVar2 = *pcVar4;
        pcVar4 = pcVar4 + 1;
      } while (cVar2 != '\0');
      pcVar8 = pcVar4 + (1 - (int)(param_1 + 0x1d5));
      FUN__text__00548e1c(((uint)(pcVar4 + (4 - (int)(param_1 + 0x1d5))) & 0x3fffc) * 0x4000 +
                          0x10000 & 0x7fff0000 | 0xfffe);
      FUN__text__00548e1c(0x454c4946);
      *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 8;
      if ((char *)0x3 < pcVar8) {
        local_c[0] = (char *)((uint)pcVar8 >> 2);
        do {
          FUN__text__00548e1c(*(undefined4 *)local_c[1]);
          *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
          local_c[1] = local_c[1] + 4;
          pcVar8 = pcVar8 + -4;
          local_c[0] = local_c[0] + -1;
        } while (local_c[0] != (char *)0x0);
      }
      if (pcVar8 != (char *)0x0) {
        local_c[0] = (char *)0x0;
        pcVar4 = local_c[1];
        ppcVar9 = local_c;
        for (uVar5 = (uint)pcVar8 >> 2; uVar5 != 0; uVar5 = uVar5 - 1) {
          *ppcVar9 = *(char **)pcVar4;
          pcVar4 = pcVar4 + 4;
          ppcVar9 = ppcVar9 + 1;
        }
        for (uVar5 = (uint)pcVar8 & 3; uVar5 != 0; uVar5 = uVar5 - 1) {
          *(char *)ppcVar9 = *pcVar4;
          pcVar4 = pcVar4 + 1;
          ppcVar9 = (char **)((int)ppcVar9 + 1);
        }
        FUN__text__00548e1c(local_c[0]);
        *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
      }
      pcVar4 = param_1 + 0x1d4;
      iVar3 = 0x2d8 - (int)pcVar4;
      do {
        cVar2 = *pcVar4;
        pcVar4[(int)(param_1 + iVar3)] = cVar2;
        pcVar4 = pcVar4 + 1;
      } while (cVar2 != '\0');
    }
    if (*(int *)(param_1 + 0x2d4) != *(int *)(param_1 + 0x1d0)) {
      FUN__text__00548e1c(0x2fffe);
      FUN__text__00548e1c(0x454e494c);
      FUN__text__00548e1c(*(undefined4 *)(param_1 + 0x1d0));
      *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 0xc;
      *(undefined4 *)(param_1 + 0x2d4) = *(undefined4 *)(param_1 + 0x1d0);
    }
  }
  return;
}

