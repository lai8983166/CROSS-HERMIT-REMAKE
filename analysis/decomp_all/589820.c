
void * FUN__text__00589820(void)

{
  int iVar1;
  undefined *puVar2;
  size_t sVar3;
  size_t sVar4;
  size_t sVar5;
  size_t sVar6;
  size_t sVar7;
  void *pvVar8;
  char *pcVar9;
  int local_18;
  uint local_14;
  int local_c;
  
  puVar2 = PTR_PTR_00765160;
  local_c = 0;
  for (local_14 = 0; local_14 < 7; local_14 = local_14 + 1) {
    sVar3 = _strlen(*(char **)(puVar2 + local_14 * 4));
    sVar4 = _strlen(*(char **)(puVar2 + local_14 * 4 + 0x1c));
    local_c = sVar4 + local_c + 2 + sVar3;
  }
  for (local_14 = 0; local_14 < 0xc; local_14 = local_14 + 1) {
    sVar3 = _strlen(*(char **)(puVar2 + local_14 * 4 + 0x38));
    sVar4 = _strlen(*(char **)(puVar2 + local_14 * 4 + 0x68));
    local_c = sVar4 + local_c + 2 + sVar3;
  }
  sVar3 = _strlen(*(char **)(puVar2 + 0x98));
  sVar4 = _strlen(*(char **)(puVar2 + 0x9c));
  sVar5 = _strlen(*(char **)(puVar2 + 0xa0));
  sVar6 = _strlen(*(char **)(puVar2 + 0xa4));
  sVar7 = _strlen(*(char **)(puVar2 + 0xa8));
  pvVar8 = _malloc(sVar4 + local_c + sVar3 + sVar5 + sVar6 + sVar7 + 0xb1);
  if (pvVar8 != (void *)0x0) {
    local_18 = (int)pvVar8 + 0xac;
    FUN__text__0056d4d0(pvVar8,PTR_PTR_00765160,0xac);
    for (local_14 = 0; local_14 < 7; local_14 = local_14 + 1) {
      *(int *)((int)pvVar8 + local_14 * 4) = local_18;
      pcVar9 = (char *)FUN__text__0056cd90(local_18,*(undefined4 *)(puVar2 + local_14 * 4));
      sVar3 = _strlen(pcVar9);
      iVar1 = local_18 + 1 + sVar3;
      *(int *)((int)pvVar8 + local_14 * 4 + 0x1c) = iVar1;
      pcVar9 = (char *)FUN__text__0056cd90(iVar1,*(undefined4 *)(puVar2 + local_14 * 4 + 0x1c));
      sVar3 = _strlen(pcVar9);
      local_18 = iVar1 + 1 + sVar3;
    }
    for (local_14 = 0; local_14 < 0xc; local_14 = local_14 + 1) {
      *(int *)((int)pvVar8 + local_14 * 4 + 0x38) = local_18;
      pcVar9 = (char *)FUN__text__0056cd90(local_18,*(undefined4 *)(puVar2 + local_14 * 4 + 0x38));
      sVar3 = _strlen(pcVar9);
      iVar1 = local_18 + 1 + sVar3;
      *(int *)((int)pvVar8 + local_14 * 4 + 0x68) = iVar1;
      pcVar9 = (char *)FUN__text__0056cd90(iVar1,*(undefined4 *)(puVar2 + local_14 * 4 + 0x68));
      sVar3 = _strlen(pcVar9);
      local_18 = iVar1 + 1 + sVar3;
    }
    *(int *)((int)pvVar8 + 0x98) = local_18;
    pcVar9 = (char *)FUN__text__0056cd90(local_18,*(undefined4 *)(puVar2 + 0x98));
    sVar3 = _strlen(pcVar9);
    iVar1 = local_18 + 1 + sVar3;
    *(int *)((int)pvVar8 + 0x9c) = iVar1;
    pcVar9 = (char *)FUN__text__0056cd90(iVar1,*(undefined4 *)(puVar2 + 0x9c));
    sVar3 = _strlen(pcVar9);
    iVar1 = iVar1 + 1 + sVar3;
    *(int *)((int)pvVar8 + 0xa0) = iVar1;
    pcVar9 = (char *)FUN__text__0056cd90(iVar1,*(undefined4 *)(puVar2 + 0xa0));
    sVar3 = _strlen(pcVar9);
    iVar1 = iVar1 + 1 + sVar3;
    *(int *)((int)pvVar8 + 0xa4) = iVar1;
    pcVar9 = (char *)FUN__text__0056cd90(iVar1,*(undefined4 *)(puVar2 + 0xa4));
    sVar3 = _strlen(pcVar9);
    *(size_t *)((int)pvVar8 + 0xa8) = iVar1 + 1 + sVar3;
  }
  return pvVar8;
}

