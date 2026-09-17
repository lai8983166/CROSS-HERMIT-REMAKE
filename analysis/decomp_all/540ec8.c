
uint FUN__text__00540ec8(void)

{
  char cVar1;
  int iVar2;
  char *pcVar3;
  int *piVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined4 *puVar8;
  int extraout_ECX;
  int iVar9;
  int unaff_EBP;
  undefined4 *puVar10;
  char *pcVar11;
  undefined4 *puVar12;
  bool bVar13;
  
  FUN__text__0057158c();
  if (*(undefined4 **)(unaff_EBP + 0x1c) != (undefined4 *)0x0) {
    **(undefined4 **)(unaff_EBP + 0x1c) = 0;
  }
  if (*(undefined4 **)(unaff_EBP + 0x20) != (undefined4 *)0x0) {
    **(undefined4 **)(unaff_EBP + 0x20) = 0;
  }
  if (*(undefined4 **)(unaff_EBP + 0x24) != (undefined4 *)0x0) {
    **(undefined4 **)(unaff_EBP + 0x24) = 0;
  }
  iVar2 = *(int *)(unaff_EBP + 8);
  if ((iVar2 == 0) || (iVar5 = *(int *)(unaff_EBP + 0xc), iVar5 == 0)) {
    uVar7 = 0x8876086c;
    goto LAB__text__0054137a;
  }
  *(int *)(extraout_ECX + 0xb8) = iVar2;
  *(int *)(extraout_ECX + 0xbc) = iVar2;
  *(int *)(extraout_ECX + 0xc0) = iVar2;
  *(int *)(extraout_ECX + 0xc4) = iVar2 + iVar5;
  iVar2 = *(int *)(unaff_EBP + 0x14);
  if (iVar2 == 0) {
    iVar2 = 1;
  }
  *(int *)(extraout_ECX + 0x1d0) = iVar2;
  *(uint *)(extraout_ECX + 0xb0) = *(uint *)(unaff_EBP + 0x18) & 1;
  pcVar3 = *(char **)(unaff_EBP + 0x10);
  *(undefined4 *)(extraout_ECX + 0x3d8) = 0;
  *(undefined4 *)(extraout_ECX + 0x3dc) = 0;
  *(undefined4 *)(extraout_ECX + 0x3e0) = 0;
  *(undefined4 *)(extraout_ECX + 0x3e4) = 0;
  *(undefined4 *)(extraout_ECX + 0xac) = 0;
  *(undefined4 *)(extraout_ECX + 0xb4) = 0;
  if (pcVar3 == (char *)0x0) {
    *(undefined1 *)(extraout_ECX + 0x1d4) = 0;
    FUN__text__0053f973();
  }
  else {
    iVar2 = (extraout_ECX + 0x1d4) - (int)pcVar3;
    do {
      cVar1 = *pcVar3;
      pcVar3[iVar2] = cVar1;
      pcVar3 = pcVar3 + 1;
    } while (cVar1 != '\0');
  }
  *(undefined1 *)(extraout_ECX + 0x2d8) = 0;
  *(undefined4 *)(extraout_ECX + 0x2d4) = 0;
  pcVar3 = (char *)FUN__text__00572aa0(4,0);
  pcVar3 = __strdup(pcVar3);
  *(char **)(unaff_EBP + 8) = pcVar3;
  if (pcVar3 == (char *)0x0) {
LAB__text__00540fc7:
    FUN__text__00572aa0(4,&DAT_005d17f8);
  }
  else {
    iVar2 = 2;
    bVar13 = true;
    pcVar11 = "C";
    do {
      if (iVar2 == 0) break;
      iVar2 = iVar2 + -1;
      bVar13 = *pcVar3 == *pcVar11;
      pcVar3 = pcVar3 + 1;
      pcVar11 = pcVar11 + 1;
    } while (bVar13);
    if (!bVar13) goto LAB__text__00540fc7;
  }
  iVar2 = FUN__text__00540a0f();
  if (iVar2 != 0) {
    *(undefined4 *)(extraout_ECX + 0x98) = 1;
  }
  if (*(int *)(unaff_EBP + 8) != 0) {
    iVar2 = 2;
    bVar13 = true;
    pcVar3 = *(char **)(unaff_EBP + 8);
    pcVar11 = "C";
    do {
      if (iVar2 == 0) break;
      iVar2 = iVar2 + -1;
      bVar13 = *pcVar3 == *pcVar11;
      pcVar3 = pcVar3 + 1;
      pcVar11 = pcVar11 + 1;
    } while (bVar13);
    if (!bVar13) {
      FUN__text__00572aa0(4,*(undefined4 *)(unaff_EBP + 8));
    }
    FUN__text__0056f370(*(undefined4 *)(unaff_EBP + 8));
  }
  if (*(int *)(extraout_ECX + 0x98) != 0) goto LAB__text__00541345;
  if ((*(int *)(unaff_EBP + 0x1c) != 0) && (*(int *)(extraout_ECX + 0xac) == 0)) {
    iVar2 = FUN__text__00428a40(0x10);
    *(int *)(unaff_EBP + 8) = iVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0;
    if (iVar2 == 0) {
      piVar4 = (int *)0x0;
    }
    else {
      piVar4 = (int *)FUN__text__005493b1();
    }
    *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
    if (piVar4 != (int *)0x0) {
      iVar5 = (**(code **)(*piVar4 + 0x18))(*(undefined4 *)(extraout_ECX + 0x9c));
      *(int *)(unaff_EBP + 8) = iVar5;
      iVar2 = *piVar4;
      if (-1 < iVar5) {
        uVar6 = (**(code **)(iVar2 + 0xc))(piVar4);
        *(undefined4 *)(unaff_EBP + 0xc) = uVar6;
        while (*(int *)(extraout_ECX + 0x9c) != 0) {
          *(int *)(extraout_ECX + 0x9c) = *(int *)(extraout_ECX + 0x9c) + -4;
          FUN__text__00548e8a(*(int *)(extraout_ECX + 0x9c) + *(int *)(unaff_EBP + 0xc));
        }
        **(undefined4 **)(unaff_EBP + 0x1c) = piVar4;
        goto LAB__text__005410b1;
      }
LAB__text__0054113a:
      (**(code **)(iVar2 + 0x14))(1);
    }
LAB__text__0054113d:
    uVar7 = 0x8007000e;
    goto LAB__text__0054137a;
  }
LAB__text__005410b1:
  if (*(int *)(extraout_ECX + 0x98) == 0) {
    if (*(int *)(unaff_EBP + 0x20) != 0) {
      iVar2 = *(int *)(extraout_ECX + 0xa0);
      *(int *)(unaff_EBP + 0xc) = iVar2;
      iVar2 = iVar2 + 0x30;
      iVar5 = *(int *)(extraout_ECX + 0xac);
      pcVar3 = "D3DX8 Shader Assembler Version 0.91";
      puVar10 = (undefined4 *)(unaff_EBP + -0x30);
      for (iVar9 = 9; iVar9 != 0; iVar9 = iVar9 + -1) {
        *puVar10 = *(undefined4 *)pcVar3;
        pcVar3 = pcVar3 + 4;
        puVar10 = puVar10 + 1;
      }
      *(int *)(unaff_EBP + 0x1c) = iVar2;
      if (iVar5 != 0) {
        *(int *)(unaff_EBP + 0x1c) = iVar2 + *(int *)(extraout_ECX + 0x9c);
      }
      iVar2 = FUN__text__00428a40(0x10);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 1;
      if (iVar2 == 0) {
        piVar4 = (int *)0x0;
      }
      else {
        piVar4 = (int *)FUN__text__005493b1();
      }
      *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
      *(int **)(unaff_EBP + 0x14) = piVar4;
      *(int **)(unaff_EBP + 0x10) = piVar4;
      if (piVar4 == (int *)0x0) goto LAB__text__0054113d;
      iVar2 = (**(code **)(*piVar4 + 0x18))(*(undefined4 *)(unaff_EBP + 0x1c));
      *(int *)(unaff_EBP + 8) = iVar2;
      if (iVar2 < 0) {
        iVar2 = *piVar4;
        goto LAB__text__0054113a;
      }
      puVar8 = (undefined4 *)
               (**(code **)(**(int **)(unaff_EBP + 0x14) + 0xc))(*(int **)(unaff_EBP + 0x14));
      *puVar8 = *(undefined4 *)(extraout_ECX + 0xb4);
      puVar8[1] = 0x9fffe;
      puVar10 = puVar8 + 2;
      for (iVar2 = 9; iVar2 != 0; iVar2 = iVar2 + -1) {
        *puVar10 = 0;
        puVar10 = puVar10 + 1;
      }
      iVar5 = *(int *)(unaff_EBP + 0x1c);
      iVar2 = *(int *)(unaff_EBP + 0xc);
      puVar10 = (undefined4 *)(unaff_EBP + -0x30);
      puVar12 = puVar8 + 2;
      for (iVar9 = 9; iVar9 != 0; iVar9 = iVar9 + -1) {
        *puVar12 = *puVar10;
        puVar10 = puVar10 + 1;
        puVar12 = puVar12 + 1;
      }
      *(undefined4 *)((int)puVar8 + iVar5 + -4) = 0xffff;
      iVar5 = (int)puVar8 + iVar5 + -8;
      while (iVar2 != 0) {
        FUN__text__00548e8a(iVar5);
        iVar5 = iVar5 + -4;
        piVar4 = (int *)(unaff_EBP + 0xc);
        *piVar4 = *piVar4 + -4;
        iVar2 = *piVar4;
      }
      if (*(int *)(extraout_ECX + 0xac) != 0) {
        piVar4 = (int *)(extraout_ECX + 0x9c);
        while (*piVar4 != 0) {
          FUN__text__00548e8a(iVar5);
          iVar5 = iVar5 + -4;
          *piVar4 = *piVar4 + -4;
        }
      }
      **(undefined4 **)(unaff_EBP + 0x20) = *(undefined4 *)(unaff_EBP + 0x14);
    }
    if ((*(int *)(extraout_ECX + 0x98) == 0) && ((*(byte *)(unaff_EBP + 0x18) & 2) == 0)) {
      if (*(int *)(extraout_ECX + 0xa0) == 0) {
        FUN__text__0053eb92(extraout_ECX,"statement expected");
      }
      else {
        bVar13 = false;
        iVar2 = (*API_ADVAPI32_DLL_RegOpenKeyA)
                          (0x80000002,"SOFTWARE\\Microsoft\\Direct3D",unaff_EBP + 0x20);
        if (iVar2 == 0) {
          *(undefined4 *)(unaff_EBP + 0x1c) = 4;
          iVar2 = (*API_ADVAPI32_DLL_RegQueryValueExA)
                            (*(undefined4 *)(unaff_EBP + 0x20),"LoadDebugRuntime",0,unaff_EBP + 0x18
                             ,unaff_EBP + 0xc,unaff_EBP + 0x1c);
          if (((iVar2 == 0) && (*(int *)(unaff_EBP + 0x18) == 4)) &&
             (*(int *)(unaff_EBP + 0x1c) == 4)) {
            bVar13 = *(int *)(unaff_EBP + 0xc) != 0;
          }
          (*API_ADVAPI32_DLL_RegCloseKey)(*(undefined4 *)(unaff_EBP + 0x20));
          if ((!bVar13) ||
             ((iVar2 = (*DAT_005922c8)("d3d8d.dll"), iVar2 == 0 &&
              (iVar2 = (*DAT_00592184)("d3d8d.dll"), iVar2 == 0)))) goto LAB__text__0054126c;
        }
        else {
LAB__text__0054126c:
          iVar2 = (*DAT_005922c8)("d3d8.dll");
          if ((iVar2 == 0) && (iVar2 = (*DAT_00592184)("d3d8.dll"), iVar2 == 0))
          goto LAB__text__00541345;
        }
        uVar7 = -(uint)(*(int *)(unaff_EBP + 0x24) != 0) & unaff_EBP + 0x1cU;
        *(undefined4 *)(unaff_EBP + 0x1c) = 0;
        iVar5 = *(int *)(extraout_ECX + 0xac);
        *(uint *)(unaff_EBP + 0x18) = (uint)(*(int *)(unaff_EBP + 0x24) != 0);
        if (iVar5 == 0) {
          iVar2 = (*DAT_005922cc)(iVar2,"ValidateVertexShader");
          *(int *)(unaff_EBP + 0xc) = iVar2;
          if (iVar2 != 0) {
            uVar6 = (**(code **)(**(int **)(unaff_EBP + 0x10) + 0xc))
                              (*(int **)(unaff_EBP + 0x10),0,0,*(undefined4 *)(unaff_EBP + 0x18),
                               uVar7);
            uVar6 = (**(code **)(unaff_EBP + 0xc))(uVar6);
            goto LAB__text__005412fa;
          }
        }
        else {
          iVar2 = (*DAT_005922cc)(iVar2,"ValidatePixelShader");
          *(int *)(unaff_EBP + 0xc) = iVar2;
          if (iVar2 != 0) {
            uVar6 = (**(code **)(**(int **)(unaff_EBP + 0x10) + 0xc))
                              (*(int **)(unaff_EBP + 0x10),0,*(undefined4 *)(unaff_EBP + 0x18),uVar7
                              );
            uVar6 = (**(code **)(unaff_EBP + 0xc))(uVar6);
LAB__text__005412fa:
            *(undefined4 *)(unaff_EBP + 8) = uVar6;
          }
        }
        if (*(int *)(unaff_EBP + 8) < 0) {
          *(undefined4 *)(extraout_ECX + 0x98) = 1;
        }
        if (*(int *)(unaff_EBP + 0x1c) != 0) {
          FUN__text__00548f0a(*(undefined4 *)(unaff_EBP + 0x1c));
          uVar6 = *(undefined4 *)(unaff_EBP + 0x1c);
          *(int *)(extraout_ECX + 0xa4) = *(int *)(extraout_ECX + 0xa4) + 1;
          uVar6 = (*DAT_00592254)(0,uVar6);
          (*API_KERNEL32_DLL_HeapFree)(uVar6);
        }
      }
    }
  }
LAB__text__00541345:
  if (((*(int *)(extraout_ECX + 0xa4) == 0) || (*(int *)(unaff_EBP + 0x24) == 0)) ||
     (uVar7 = FUN__text__00548ff9(*(undefined4 *)(unaff_EBP + 0x24)), -1 < (int)uVar7)) {
    uVar7 = -(uint)(*(int *)(extraout_ECX + 0x98) != 0) & 0x88760b59;
  }
LAB__text__0054137a:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return uVar7;
}

