
uint __thiscall FUN__text__0053f529(int param_1,char *param_2,uint param_3,int param_4)

{
  char cVar1;
  int iVar2;
  int iVar3;
  char *pcVar4;
  char *pcVar5;
  char *pcVar6;
  bool bVar7;
  bool bVar8;
  bool bVar9;
  char *pcVar10;
  uint local_c;
  uint local_8;
  
  pcVar10 = param_2;
  while ((*pcVar10 != '\0' && (iVar2 = FUN__text__005717b0((int)*pcVar10), iVar2 != 0))) {
    pcVar10 = pcVar10 + 1;
  }
  cVar1 = *pcVar10;
  pcVar4 = pcVar10;
  while ((cVar1 != '\0' && (iVar2 = FUN__text__00571880((int)*pcVar4), iVar2 != 0))) {
    pcVar4 = pcVar4 + 1;
    cVar1 = *pcVar4;
  }
  bVar7 = *pcVar10 != '\0';
  bVar9 = true;
  local_8 = 0;
  local_c = 0;
  if ((*(int *)(param_1 + 0xac) != 0) && (*pcVar4 == '_')) {
    iVar2 = 6;
    bVar8 = true;
    pcVar5 = pcVar4;
    pcVar6 = "_bias";
    do {
      if (iVar2 == 0) break;
      iVar2 = iVar2 + -1;
      bVar8 = *pcVar5 == *pcVar6;
      pcVar5 = pcVar5 + 1;
      pcVar6 = pcVar6 + 1;
    } while (bVar8);
    if (bVar8) {
      local_c = 0x2000000;
      pcVar4 = pcVar4 + 5;
    }
    else {
      iVar2 = 5;
      bVar8 = true;
      pcVar5 = pcVar4;
      pcVar6 = "_bx2";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar8 = *pcVar5 == *pcVar6;
        pcVar5 = pcVar5 + 1;
        pcVar6 = pcVar6 + 1;
      } while (bVar8);
      if (bVar8) {
        local_c = 0x4000000;
        pcVar4 = pcVar4 + 4;
      }
      else {
        iVar2 = 4;
        bVar8 = true;
        iVar3 = iVar2;
        pcVar5 = pcVar4;
        pcVar6 = "_x2";
        do {
          if (iVar3 == 0) break;
          iVar3 = iVar3 + -1;
          bVar8 = *pcVar5 == *pcVar6;
          pcVar5 = pcVar5 + 1;
          pcVar6 = pcVar6 + 1;
        } while (bVar8);
        if (bVar8) {
          local_c = 0x7000000;
        }
        else {
          bVar8 = true;
          iVar3 = iVar2;
          pcVar5 = pcVar4;
          pcVar6 = "_dz";
          do {
            if (iVar3 == 0) break;
            iVar3 = iVar3 + -1;
            bVar8 = *pcVar5 == *pcVar6;
            pcVar5 = pcVar5 + 1;
            pcVar6 = pcVar6 + 1;
          } while (bVar8);
          if (!bVar8) {
            bVar8 = true;
            iVar3 = iVar2;
            pcVar5 = pcVar4;
            pcVar6 = "_db";
            do {
              if (iVar3 == 0) break;
              iVar3 = iVar3 + -1;
              bVar8 = *pcVar5 == *pcVar6;
              pcVar5 = pcVar5 + 1;
              pcVar6 = pcVar6 + 1;
            } while (bVar8);
            if (!bVar8) {
              bVar8 = true;
              iVar3 = iVar2;
              pcVar5 = pcVar4;
              pcVar6 = "_dw";
              do {
                if (iVar3 == 0) break;
                iVar3 = iVar3 + -1;
                bVar8 = *pcVar5 == *pcVar6;
                pcVar5 = pcVar5 + 1;
                pcVar6 = pcVar6 + 1;
              } while (bVar8);
              if (!bVar8) {
                bVar8 = true;
                pcVar5 = pcVar4;
                pcVar6 = "_da";
                do {
                  if (iVar2 == 0) break;
                  iVar2 = iVar2 + -1;
                  bVar8 = *pcVar5 == *pcVar6;
                  pcVar5 = pcVar5 + 1;
                  pcVar6 = pcVar6 + 1;
                } while (bVar8);
                if (!bVar8) goto LAB__text__0053f641;
              }
              local_c = 0xa000000;
              goto LAB__text__0053f63e;
            }
          }
          local_c = 0x9000000;
        }
LAB__text__0053f63e:
        pcVar4 = pcVar4 + 3;
      }
    }
  }
LAB__text__0053f641:
  if ((bVar7) && (local_8 = FUN__text__00572840(pcVar10), (local_8 & 0xffffe000) != 0)) {
    bVar9 = false;
  }
  if ((*pcVar4 == '\0') && (bVar9)) {
    if (param_4 != 0) {
      iVar2 = 2;
      bVar9 = true;
      pcVar10 = param_2;
      pcVar4 = "c";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar10 == *pcVar4;
        pcVar10 = pcVar10 + 1;
        pcVar4 = pcVar4 + 1;
      } while (bVar9);
      if ((bVar9) && (!bVar7)) {
        local_8 = local_c | param_3;
LAB__text__0053f861:
        return local_8 | 0x20000000;
      }
      goto LAB__text__0053f868;
    }
    cVar1 = *pcVar10;
    *pcVar10 = '\0';
    if (*(int *)(param_1 + 0xac) == 0) {
      iVar2 = 5;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "oPos";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (!bVar7)) {
        return 0x40000000;
      }
      iVar2 = 5;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "oPts";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (!bVar7)) {
        return 0x40000002;
      }
      iVar2 = 5;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "oFog";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (!bVar7)) {
        return 0x40000001;
      }
      iVar2 = 2;
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "v";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) goto LAB__text__0053f794;
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "r";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        return local_8;
      }
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "c";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) goto LAB__text__0053f861;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "a";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) goto LAB__text__0053f7ed;
      iVar2 = 3;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "oD";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        return local_8 | 0x50000000;
      }
      iVar2 = 3;
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "oT";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        return local_8 | 0x60000000;
      }
    }
    else {
      iVar2 = 2;
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "v";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        local_8 = local_c | local_8;
LAB__text__0053f794:
        return local_8 | 0x10000000;
      }
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "r";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        return local_c | local_8;
      }
      bVar9 = true;
      iVar3 = iVar2;
      pcVar4 = param_2;
      pcVar5 = "c";
      do {
        if (iVar3 == 0) break;
        iVar3 = iVar3 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        local_8 = local_c | local_8;
        goto LAB__text__0053f861;
      }
      bVar9 = true;
      pcVar4 = param_2;
      pcVar5 = "t";
      do {
        if (iVar2 == 0) break;
        iVar2 = iVar2 + -1;
        bVar9 = *pcVar4 == *pcVar5;
        pcVar4 = pcVar4 + 1;
        pcVar5 = pcVar5 + 1;
      } while (bVar9);
      if ((bVar9) && (bVar7)) {
        local_8 = local_c | local_8;
LAB__text__0053f7ed:
        return local_8 | 0x30000000;
      }
    }
    *pcVar10 = cVar1;
  }
  else {
LAB__text__0053f868:
    if (param_4 != 0) {
      if ((param_3 & 0x2000) == 0) {
        pcVar10 = "invalid register \'%s[%d]\'";
      }
      else {
        pcVar10 = "invalid register \'%s[a0.x + %d]\'";
      }
      FUN__text__0053eb92(param_1,pcVar10,param_2,param_3 & 0x1fff);
      goto LAB__text__0053f8b4;
    }
  }
  FUN__text__0053eb92(param_1,"invalid register \'%s\'",param_2);
LAB__text__0053f8b4:
  *(undefined4 *)(param_1 + 0x98) = 1;
  return 0;
}

