
undefined8 __fastcall
FUN__adata__0085eb04(undefined4 param_1,undefined4 param_2,short *param_3,char *param_4)

{
  char cVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  char *pcVar6;
  char *pcVar7;
  char *pcVar8;
  bool bVar9;
  
  if ((*param_3 == 0x5a4d) && (*(int *)((int)param_3 + *(int *)(param_3 + 0x1e)) == 0x4550)) {
    iVar3 = 0x96;
    pcVar6 = param_4;
    do {
      pcVar7 = pcVar6;
      if (iVar3 == 0) break;
      iVar3 = iVar3 + -1;
      pcVar7 = pcVar6 + 1;
      cVar1 = *pcVar6;
      pcVar6 = pcVar7;
    } while (cVar1 != '\0');
    iVar3 = ((int *)((int)param_3 + *(int *)(param_3 + 0x1e)))[0x1e];
    piVar5 = (int *)(*(int *)((int)param_3 + iVar3 + 0x20) + (int)param_3);
    iVar2 = 0;
    do {
      bVar9 = (char *)(*piVar5 + (int)param_3) == (char *)0x0;
      iVar4 = (int)pcVar7 - (int)param_4;
      pcVar6 = param_4;
      pcVar8 = (char *)(*piVar5 + (int)param_3);
      do {
        if (iVar4 == 0) break;
        iVar4 = iVar4 + -1;
        bVar9 = *pcVar6 == *pcVar8;
        pcVar6 = pcVar6 + 1;
        pcVar8 = pcVar8 + 1;
      } while (bVar9);
      if (bVar9) break;
      piVar5 = piVar5 + 1;
      iVar2 = iVar2 + 1;
    } while (iVar2 != *(int *)((int)param_3 + iVar3 + 0x18));
    if (iVar2 != *(int *)((int)param_3 + iVar3 + 0x18)) {
      iVar3 = *(int *)((int)param_3 +
                      *(int *)((int)param_3 + iVar3 + 0x1c) +
                      (uint)*(ushort *)
                             ((int)param_3 + iVar2 * 2 + *(int *)((int)param_3 + iVar3 + 0x24)) * 4)
              + (int)param_3;
      goto LAB__adata__0085ebab;
    }
  }
  iVar3 = 0;
LAB__adata__0085ebab:
  return CONCAT44(param_2,iVar3);
}

