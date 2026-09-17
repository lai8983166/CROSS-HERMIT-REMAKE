
undefined1 * FUN__text__005896f0(void)

{
  undefined *puVar1;
  size_t sVar2;
  size_t sVar3;
  undefined1 *puVar4;
  char *pcVar5;
  undefined1 *local_18;
  uint local_14;
  int local_c;
  
  puVar1 = PTR_PTR_00765160;
  local_c = 0;
  for (local_14 = 0; local_14 < 0xc; local_14 = local_14 + 1) {
    sVar2 = _strlen(*(char **)(puVar1 + local_14 * 4 + 0x38));
    sVar3 = _strlen(*(char **)(puVar1 + local_14 * 4 + 0x68));
    local_c = sVar3 + local_c + 2 + sVar2;
  }
  puVar4 = _malloc(local_c + 1);
  if (puVar4 != (undefined1 *)0x0) {
    local_18 = puVar4;
    for (local_14 = 0; local_14 < 0xc; local_14 = local_14 + 1) {
      *local_18 = 0x3a;
      local_18 = local_18 + 1;
      pcVar5 = (char *)FUN__text__0056cd90(local_18,*(undefined4 *)(puVar1 + local_14 * 4 + 0x38));
      sVar2 = _strlen(pcVar5);
      local_18 = local_18 + sVar2;
      *local_18 = 0x3a;
      pcVar5 = (char *)FUN__text__0056cd90(local_18 + 1,
                                           *(undefined4 *)(puVar1 + local_14 * 4 + 0x68));
      sVar2 = _strlen(pcVar5);
      local_18 = local_18 + 1 + sVar2;
    }
    *local_18 = 0;
  }
  return puVar4;
}

