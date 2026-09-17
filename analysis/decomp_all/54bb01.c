
undefined4 FUN__text__0054bb01(undefined4 *param_1)

{
  int *piVar1;
  char *pcVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  uint uVar6;
  char *pcVar7;
  undefined4 uVar8;
  
  puVar5 = param_1;
  if ((param_1 == (undefined4 *)0x0) || (piVar1 = (int *)param_1[7], piVar1 == (int *)0x0)) {
    uVar8 = 0xfffffffe;
  }
  else {
    if (*piVar1 != 0xd) {
      *piVar1 = 0xd;
      *(undefined4 *)(param_1[7] + 4) = 0;
    }
    if (param_1[1] == 0) {
      uVar8 = 0xfffffffb;
    }
    else {
      pcVar2 = (char *)*param_1;
      iVar3 = param_1[7];
      uVar6 = *(uint *)(iVar3 + 4);
      pcVar7 = pcVar2;
      param_1 = (undefined4 *)param_1[1];
      do {
        if (3 < uVar6) break;
        if (*pcVar7 == (&DAT_005d3670)[uVar6]) {
          uVar6 = uVar6 + 1;
        }
        else if (*pcVar7 == '\0') {
          uVar6 = 4 - uVar6;
        }
        else {
          uVar6 = 0;
        }
        pcVar7 = pcVar7 + 1;
        param_1 = (undefined4 *)((int)param_1 + -1);
      } while (param_1 != (undefined4 *)0x0);
      puVar5[2] = pcVar7 + (puVar5[2] - (int)pcVar2);
      *puVar5 = pcVar7;
      puVar5[1] = param_1;
      *(uint *)(iVar3 + 4) = uVar6;
      if (uVar6 == 4) {
        uVar8 = puVar5[2];
        uVar4 = puVar5[5];
        FUN__text__0054b5a8(puVar5);
        puVar5[2] = uVar8;
        puVar5[5] = uVar4;
        *(undefined4 *)puVar5[7] = 7;
        uVar8 = 0;
      }
      else {
        uVar8 = 0xfffffffd;
      }
    }
  }
  return uVar8;
}

