
void __thiscall FUN__text__0054cdba(undefined4 param_1,int param_2)

{
  uint *puVar1;
  byte bVar2;
  int iVar3;
  uint uVar4;
  undefined4 uVar5;
  char *pcVar6;
  int iVar7;
  undefined4 local_4;
  
  iVar3 = param_2;
  puVar1 = (uint *)(param_2 + 0xd4);
  *puVar1 = *puVar1 + 1;
  if (*(uint *)(param_2 + 0xc0) <= *puVar1) {
    local_4 = param_1;
    if (*(char *)(param_2 + 0x113) != '\0') {
      *puVar1 = 0;
      FUN__text__0054bc92(param_2,*(undefined4 *)(param_2 + 0xd8),0,*(int *)(param_2 + 200) + 1);
      do {
        *(char *)(iVar3 + 0x114) = *(char *)(iVar3 + 0x114) + '\x01';
        bVar2 = *(byte *)(iVar3 + 0x114);
        if (6 < bVar2) goto LAB__text__0054ce87;
        iVar7 = (uint)bVar2 * 4;
        uVar4 = ((*(int *)(iVar3 + 0xb8) - *(int *)(&DAT_005d3684 + iVar7)) + -1 +
                *(uint *)(&DAT_005d36a0 + iVar7)) / *(uint *)(&DAT_005d36a0 + iVar7);
        *(uint *)(iVar3 + 0xd0) = uVar4;
        *(uint *)(iVar3 + 0xcc) = (*(byte *)(iVar3 + 0x119) * uVar4 + 7 >> 3) + 1;
      } while (((*(byte *)(iVar3 + 0x60) & 2) == 0) &&
              (*(uint *)(iVar3 + 0xc0) =
                    ((*(int *)(iVar3 + 0xbc) - *(int *)(&DAT_005d36bc + iVar7)) + -1 +
                    *(uint *)(&DAT_005d36d8 + iVar7)) / *(uint *)(&DAT_005d36d8 + iVar7),
              *(int *)(iVar3 + 0xd0) == 0));
      if (bVar2 < 7) {
        return;
      }
    }
LAB__text__0054ce87:
    if ((*(byte *)(iVar3 + 0x5c) & 0x20) == 0) {
      *(int **)(iVar3 + 0x70) = &param_2;
      *(undefined4 *)(iVar3 + 0x74) = 1;
      while( true ) {
        if (*(int *)(iVar3 + 0x68) == 0) {
          if (*(int *)(iVar3 + 0xfc) == 0) {
            do {
              FUN__text__0054c5c9(iVar3,0);
              FUN__text__00546578(iVar3,&local_4,4);
              uVar5 = FUN__text__0054bcc3(&local_4);
              *(undefined4 *)(iVar3 + 0xfc) = uVar5;
              FUN__text__005466ca(iVar3);
              FUN__text__0054bcf9(iVar3,(int *)(iVar3 + 0x10c),4);
              if (*(int *)(iVar3 + 0x10c) != DAT_005d36f4) {
                FUN__text__0054381d(iVar3,"Not enough image data");
              }
            } while (*(int *)(iVar3 + 0xfc) == 0);
          }
          *(uint *)(iVar3 + 0x68) = *(uint *)(iVar3 + 0xa0);
          *(undefined4 *)(iVar3 + 100) = *(undefined4 *)(iVar3 + 0x9c);
          if (*(uint *)(iVar3 + 0xfc) < *(uint *)(iVar3 + 0xa0)) {
            *(uint *)(iVar3 + 0x68) = *(uint *)(iVar3 + 0xfc);
          }
          FUN__text__0054bcf9(iVar3,*(undefined4 *)(iVar3 + 0x9c),*(undefined4 *)(iVar3 + 0x68));
          *(int *)(iVar3 + 0xfc) = *(int *)(iVar3 + 0xfc) - *(int *)(iVar3 + 0x68);
        }
        iVar7 = FUN__text__0054b721((undefined4 *)(iVar3 + 100),1);
        if (iVar7 == 1) break;
        if (iVar7 != 0) {
          pcVar6 = *(char **)(iVar3 + 0x7c);
          if (pcVar6 == (char *)0x0) {
            pcVar6 = "Decompression Error";
          }
          FUN__text__0054381d(iVar3,pcVar6);
        }
        if (*(int *)(iVar3 + 0x74) == 0) {
          FUN__text__0054381d(iVar3,"Extra compressed data");
        }
      }
      if (((*(int *)(iVar3 + 0x74) == 0) || (*(int *)(iVar3 + 0x68) != 0)) ||
         (*(int *)(iVar3 + 0xfc) != 0)) {
        FUN__text__0054381d(iVar3,"Extra compressed data");
      }
      *(uint *)(iVar3 + 0x58) = *(uint *)(iVar3 + 0x58) | 8;
      *(uint *)(iVar3 + 0x5c) = *(uint *)(iVar3 + 0x5c) | 0x20;
      *(undefined4 *)(iVar3 + 0x74) = 0;
    }
    if ((*(int *)(iVar3 + 0xfc) != 0) || (*(int *)(iVar3 + 0x68) != 0)) {
      FUN__text__0054381d(iVar3,"Extra compression data");
    }
    FUN__text__0054b5a8(iVar3 + 100);
    *(uint *)(iVar3 + 0x58) = *(uint *)(iVar3 + 0x58) | 8;
  }
  return;
}

