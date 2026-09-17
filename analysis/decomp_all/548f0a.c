
undefined4 __thiscall FUN__text__00548f0a(int *param_1,char *param_2)

{
  char cVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  char *pcVar7;
  undefined4 *puVar8;
  undefined4 *puVar9;
  char *pcVar10;
  
  if (param_1[1] == param_1[2]) {
    puVar2 = (undefined4 *)FUN__text__00428a40(param_1[2] * 4 + 0x40);
    if (puVar2 != (undefined4 *)0x0) {
      if ((undefined4 *)*param_1 != (undefined4 *)0x0) {
        puVar8 = (undefined4 *)*param_1;
        puVar9 = puVar2;
        for (uVar4 = param_1[1] & 0x3fffffff; uVar4 != 0; uVar4 = uVar4 - 1) {
          *puVar9 = *puVar8;
          puVar8 = puVar8 + 1;
          puVar9 = puVar9 + 1;
        }
        for (iVar5 = 0; iVar5 != 0; iVar5 = iVar5 + -1) {
          *(undefined1 *)puVar9 = *(undefined1 *)puVar8;
          puVar8 = (undefined4 *)((int)puVar8 + 1);
          puVar9 = (undefined4 *)((int)puVar9 + 1);
        }
        FUN__text__00428ad0(*param_1);
      }
      param_1[2] = param_1[2] + 0x10;
      *param_1 = (int)puVar2;
      goto LAB__text__00548f56;
    }
LAB__text__00548f7b:
    uVar3 = 0x8007000e;
    param_1[3] = -0x7ff8fff2;
  }
  else {
LAB__text__00548f56:
    if (param_2 == (char *)0x0) {
      *(undefined4 *)(*param_1 + param_1[1] * 4) = 0;
    }
    else {
      pcVar7 = param_2;
      do {
        cVar1 = *pcVar7;
        pcVar7 = pcVar7 + 1;
      } while (cVar1 != '\0');
      uVar4 = (int)pcVar7 - (int)(param_2 + 1);
      pcVar7 = (char *)FUN__text__00428a40(uVar4 + 1);
      if (pcVar7 == (char *)0x0) goto LAB__text__00548f7b;
      pcVar10 = pcVar7;
      for (uVar6 = uVar4 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
        *(undefined4 *)pcVar10 = *(undefined4 *)param_2;
        param_2 = param_2 + 4;
        pcVar10 = pcVar10 + 4;
      }
      for (uVar6 = uVar4 & 3; uVar6 != 0; uVar6 = uVar6 - 1) {
        *pcVar10 = *param_2;
        param_2 = param_2 + 1;
        pcVar10 = pcVar10 + 1;
      }
      pcVar7[uVar4] = '\0';
      param_1[4] = param_1[4] + uVar4;
      *(char **)(*param_1 + param_1[1] * 4) = pcVar7;
    }
    param_1[1] = param_1[1] + 1;
    uVar3 = 0;
  }
  return uVar3;
}

