
undefined4 __thiscall FUN__text__0054923e(int param_1,char *param_2)

{
  char cVar1;
  int iVar2;
  char *pcVar3;
  int iVar4;
  uint uVar5;
  undefined4 *puVar6;
  int *piVar7;
  uint uVar8;
  undefined4 *puVar9;
  undefined4 *puVar10;
  undefined4 *puVar11;
  uint local_8;
  
  pcVar3 = param_2;
  do {
    cVar1 = *pcVar3;
    pcVar3 = pcVar3 + 1;
  } while (cVar1 != '\0');
  iVar4 = (int)pcVar3 - (int)(param_2 + 1);
  if ((*(int *)(param_1 + 0x14) - iVar4) - 1U < *(int *)(param_1 + 0x10) + 4U) {
    iVar2 = *(int *)(param_1 + 8);
    uVar5 = __ftol();
    local_8 = iVar2 + iVar4;
    if (local_8 <= uVar5) {
      local_8 = uVar5;
    }
    puVar6 = (undefined4 *)FUN__text__00428a40(local_8 + 3 & 0xfffffffc);
    if (puVar6 == (undefined4 *)0x0) {
      return 0x8007000e;
    }
    uVar8 = (*(int *)(param_1 + 0xc) - (int)*(undefined4 **)(param_1 + 0x14)) +
            *(int *)(param_1 + 8);
    puVar9 = (undefined4 *)((int)puVar6 + (local_8 - uVar8));
    puVar10 = *(undefined4 **)(param_1 + 0x14);
    puVar11 = puVar9;
    for (uVar5 = uVar8 >> 2; uVar5 != 0; uVar5 = uVar5 - 1) {
      *puVar11 = *puVar10;
      puVar10 = puVar10 + 1;
      puVar11 = puVar11 + 1;
    }
    for (uVar8 = uVar8 & 3; uVar8 != 0; uVar8 = uVar8 - 1) {
      *(undefined1 *)puVar11 = *(undefined1 *)puVar10;
      puVar10 = (undefined4 *)((int)puVar10 + 1);
      puVar11 = (undefined4 *)((int)puVar11 + 1);
    }
    iVar2 = *(int *)(param_1 + 0x14);
    puVar10 = puVar6;
    for (piVar7 = *(int **)(param_1 + 0xc); piVar7 < *(int **)(param_1 + 0x10); piVar7 = piVar7 + 1)
    {
      *puVar10 = (undefined1 *)((int)puVar9 + (*piVar7 - iVar2));
      puVar10 = puVar10 + 1;
    }
    FUN__text__00428ad0(*(undefined4 *)(param_1 + 0xc));
    *(undefined4 **)(param_1 + 0xc) = puVar6;
    *(uint *)(param_1 + 8) = local_8;
    *(undefined4 **)(param_1 + 0x10) = puVar10;
    *(undefined4 **)(param_1 + 0x14) = puVar9;
  }
  *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + (-1 - iVar4);
  pcVar3 = *(char **)(param_1 + 0x14);
  do {
    cVar1 = *param_2;
    param_2 = param_2 + 1;
    *pcVar3 = cVar1;
    pcVar3 = pcVar3 + 1;
  } while (cVar1 != '\0');
  **(undefined4 **)(param_1 + 0x10) = *(undefined4 *)(param_1 + 0x14);
  *(int *)(param_1 + 0x10) = *(int *)(param_1 + 0x10) + 4;
  return 0;
}

