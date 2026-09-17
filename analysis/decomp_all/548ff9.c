
undefined4 FUN__text__00548ff9(void)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  int *piVar4;
  char *pcVar5;
  int *extraout_ECX;
  char *pcVar6;
  uint uVar7;
  uint uVar8;
  int unaff_EBP;
  char *pcVar9;
  
  FUN__text__0057158c();
  **(undefined4 **)(unaff_EBP + 8) = 0;
  if (extraout_ECX[4] == 0) {
    uVar2 = 0;
  }
  else {
    iVar3 = FUN__text__00428a40(0x10);
    *(int *)(unaff_EBP + -0x18) = iVar3;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    if (iVar3 == 0) {
      *(undefined4 *)(unaff_EBP + -0x14) = 0;
      piVar4 = (int *)0x0;
    }
    else {
      piVar4 = (int *)FUN__text__005493b1();
      *(int **)(unaff_EBP + -0x14) = piVar4;
    }
    *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
    if (piVar4 == (int *)0x0) {
      uVar2 = 0x8007000e;
    }
    else {
      iVar3 = (**(code **)(*piVar4 + 0x18))(extraout_ECX[1] + 1 + extraout_ECX[4]);
      *(int *)(unaff_EBP + -0x10) = iVar3;
      if (iVar3 < 0) {
        (**(code **)(*piVar4 + 0x14))(1);
        uVar2 = *(undefined4 *)(unaff_EBP + -0x10);
      }
      else {
        pcVar5 = (char *)(**(code **)(*piVar4 + 0xc))(piVar4);
        iVar3 = extraout_ECX[1];
        *(undefined4 *)(unaff_EBP + -0x10) = 0;
        if (iVar3 != 0) {
          do {
            pcVar9 = *(char **)(*extraout_ECX + *(int *)(unaff_EBP + -0x10) * 4);
            if (pcVar9 != (char *)0x0) {
              pcVar6 = pcVar9;
              do {
                cVar1 = *pcVar6;
                pcVar6 = pcVar6 + 1;
              } while (cVar1 != '\0');
              uVar7 = (int)pcVar6 - (int)(pcVar9 + 1);
              *(uint *)(unaff_EBP + -0x18) = uVar7;
              pcVar6 = pcVar5;
              for (uVar8 = uVar7 >> 2; uVar8 != 0; uVar8 = uVar8 - 1) {
                *(undefined4 *)pcVar6 = *(undefined4 *)pcVar9;
                pcVar9 = pcVar9 + 4;
                pcVar6 = pcVar6 + 4;
              }
              for (uVar8 = uVar7 & 3; uVar8 != 0; uVar8 = uVar8 - 1) {
                *pcVar6 = *pcVar9;
                pcVar9 = pcVar9 + 1;
                pcVar6 = pcVar6 + 1;
              }
              piVar4 = *(int **)(unaff_EBP + -0x14);
              pcVar5[uVar7] = '\n';
              pcVar5 = pcVar5 + uVar7 + 1;
            }
            *(int *)(unaff_EBP + -0x10) = *(int *)(unaff_EBP + -0x10) + 1;
          } while (*(uint *)(unaff_EBP + -0x10) < (uint)extraout_ECX[1]);
        }
        *pcVar5 = '\0';
        **(undefined4 **)(unaff_EBP + 8) = piVar4;
        uVar2 = 0;
      }
    }
  }
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar2;
}

