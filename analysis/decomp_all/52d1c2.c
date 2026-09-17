
int FUN__text__0052d1c2(void)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  int *extraout_ECX;
  undefined *puVar5;
  undefined4 *puVar6;
  int unaff_EBP;
  undefined4 *puVar7;
  undefined4 *puVar8;
  
  FUN__text__0057158c();
  *(int **)(unaff_EBP + -0x20) = extraout_ECX;
  FUN__text__0053b6ae();
  iVar4 = *(int *)(unaff_EBP + 0xc);
  *(undefined4 *)(unaff_EBP + -4) = 0;
  if (iVar4 == 0) {
LAB__text__0052d217:
    puVar5 = &DAT_0075dda8;
LAB__text__0052d21c:
    uVar1 = FUN__text__00526c46(*extraout_ECX);
    iVar2 = FUN__text__00526cdf(puVar5,extraout_ECX[2],uVar1);
    *(int *)(unaff_EBP + -0x1c) = iVar2;
    if (iVar2 != 0) {
      if (iVar2 != *extraout_ECX) {
        FUN__text__0052d690();
        *(undefined1 *)(unaff_EBP + -4) = 1;
        iVar2 = FUN__text__00526c46(iVar2);
        uVar3 = *(uint *)(iVar2 + 8) >> 3;
        *(uint *)(unaff_EBP + -0x10) = uVar3;
        *(int **)(unaff_EBP + -0x14) = extraout_ECX;
        do {
          puVar6 = *(undefined4 **)(unaff_EBP + -0x14);
          if (puVar6 != (undefined4 *)0x0) {
            do {
              iVar4 = FUN__text__00428a40(puVar6[5] * puVar6[3] * uVar3 * puVar6[4]);
              *(int *)(unaff_EBP + -0x18) = iVar4;
              if (iVar4 == 0) {
                *(undefined1 *)(unaff_EBP + -4) = 0;
                FUN__text__0052d69a();
                iVar2 = -0x7ff8fff2;
                goto LAB__text__0052d46c;
              }
              *(undefined4 *)(unaff_EBP + -0xd4) = puVar6[1];
              *(undefined4 *)(unaff_EBP + -0xd0) = *puVar6;
              *(undefined4 *)(unaff_EBP + -0xcc) = puVar6[0xc];
              *(undefined4 *)(unaff_EBP + -200) = puVar6[0xd];
              puVar7 = puVar6 + 6;
              puVar8 = (undefined4 *)(unaff_EBP + -0xc4);
              for (iVar4 = 6; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = *puVar7;
                puVar7 = puVar7 + 1;
                puVar8 = puVar8 + 1;
              }
              puVar7 = puVar6 + 6;
              puVar8 = (undefined4 *)(unaff_EBP + -0xac);
              for (iVar4 = 6; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = *puVar7;
                puVar7 = puVar7 + 1;
                puVar8 = puVar8 + 1;
              }
              *(undefined4 *)(unaff_EBP + -0x90) = 0;
              *(undefined4 *)(unaff_EBP + -0x94) = 1;
              *(undefined4 *)(unaff_EBP + -0x8c) = puVar6[2];
              *(undefined4 *)(unaff_EBP + -0x88) = *(undefined4 *)(unaff_EBP + -0x18);
              *(undefined4 *)(unaff_EBP + -0x84) = *(undefined4 *)(unaff_EBP + -0x1c);
              *(int *)(unaff_EBP + -0x80) = puVar6[3] * *(int *)(unaff_EBP + -0x10);
              *(int *)(unaff_EBP + -0x7c) = puVar6[3] * *(int *)(unaff_EBP + -0x10) * puVar6[4];
              *(undefined4 *)(unaff_EBP + -0x78) = 0;
              *(undefined4 *)(unaff_EBP + -0x74) = 0;
              *(undefined4 *)(unaff_EBP + -0x70) = puVar6[3];
              *(undefined4 *)(unaff_EBP + -0x6c) = puVar6[4];
              *(undefined4 *)(unaff_EBP + -0x68) = 0;
              *(undefined4 *)(unaff_EBP + -100) = puVar6[5];
              puVar7 = (undefined4 *)(unaff_EBP + -0x78);
              puVar8 = (undefined4 *)(unaff_EBP + -0x60);
              for (iVar4 = 6; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = *puVar7;
                puVar7 = puVar7 + 1;
                puVar8 = puVar8 + 1;
              }
              *(undefined4 *)(unaff_EBP + -0x44) = 0;
              *(undefined4 *)(unaff_EBP + -0x48) = 1;
              *(undefined4 *)(unaff_EBP + -0x40) = puVar6[2];
              iVar2 = FUN__text__00530f28(unaff_EBP + -0x88,unaff_EBP + -0xd4,0x80001);
              if (iVar2 < 0) {
                FUN__text__00428ad0(*(undefined4 *)(unaff_EBP + -0x18));
                *(undefined1 *)(unaff_EBP + -4) = 0;
                FUN__text__0052d69a();
                goto LAB__text__0052d46c;
              }
              if ((puVar6[1] != 0) && (puVar6[0xe] != 0)) {
                FUN__text__00428ad0(puVar6[1]);
                puVar6[1] = 0;
              }
              *puVar6 = *(undefined4 *)(unaff_EBP + -0x1c);
              puVar6[1] = *(undefined4 *)(unaff_EBP + -0x18);
              puVar7 = (undefined4 *)(unaff_EBP + -0x60);
              puVar8 = puVar6 + 6;
              for (iVar4 = 6; iVar4 != 0; iVar4 = iVar4 + -1) {
                *puVar8 = *puVar7;
                puVar7 = puVar7 + 1;
                puVar8 = puVar8 + 1;
              }
              puVar6[0xc] = *(undefined4 *)(unaff_EBP + -0x80);
              puVar6[0xd] = *(undefined4 *)(unaff_EBP + -0x7c);
              uVar3 = *(uint *)(unaff_EBP + -0x10);
              puVar6[0xe] = 1;
              puVar6 = (undefined4 *)puVar6[0x13];
            } while (puVar6 != (undefined4 *)0x0);
            iVar4 = *(int *)(unaff_EBP + 0xc);
          }
          iVar2 = *(int *)(*(int *)(unaff_EBP + -0x14) + 0x50);
          *(int *)(unaff_EBP + -0x14) = iVar2;
        } while (iVar2 != 0);
        *(undefined1 *)(unaff_EBP + -4) = 0;
        FUN__text__0052d69a();
      }
      iVar2 = FUN__text__0053b7d0(*(undefined4 *)(unaff_EBP + 8),*(undefined4 *)(unaff_EBP + 0x10));
      if (iVar2 < 0) goto LAB__text__0052d46c;
      if (iVar4 == 0) {
        uVar1 = 1;
LAB__text__0052d45c:
        iVar2 = FUN__text__0052b910(*(undefined4 *)(unaff_EBP + -0x3c),uVar1);
      }
      else {
        if (iVar4 != 4) {
          if (iVar4 != 6) {
            iVar2 = -0x7fffbfff;
            goto LAB__text__0052d46c;
          }
          uVar1 = 0;
          goto LAB__text__0052d45c;
        }
        iVar2 = FUN__text__0052cf1a(*(undefined4 *)(unaff_EBP + -0x3c));
      }
      if (-1 < iVar2) {
        iVar2 = 0;
      }
      goto LAB__text__0052d46c;
    }
  }
  else {
    if (iVar4 < 1) {
LAB__text__0052d402:
      iVar2 = -0x7789f794;
      goto LAB__text__0052d46c;
    }
    if (3 < iVar4) {
      if (iVar4 == 4) {
        puVar5 = &DAT_0075ddc0;
        goto LAB__text__0052d21c;
      }
      if (iVar4 != 5) {
        if (iVar4 == 6) goto LAB__text__0052d217;
        goto LAB__text__0052d402;
      }
    }
  }
  iVar2 = -0x7789f4a7;
LAB__text__0052d46c:
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  FUN__text__0053b8db();
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return iVar2;
}

