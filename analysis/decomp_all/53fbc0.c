
char * __fastcall FUN__text__0053fbc0(int param_1)

{
  char cVar1;
  char *pcVar2;
  int iVar3;
  char *pcVar4;
  uint uVar5;
  uint uVar6;
  char *pcVar7;
  int iVar8;
  undefined4 *puVar9;
  char *pcVar10;
  undefined4 *puVar11;
  bool bVar12;
  char local_114 [256];
  char *local_14;
  char local_d;
  char *local_c;
  char *local_8;
  
  *(undefined4 *)(param_1 + 0x3d8) = 0;
LAB__text__0053fe8e:
  while( true ) {
    while( true ) {
      uVar5 = *(uint *)(param_1 + 0xc0);
      if (*(uint *)(param_1 + 0xc4) <= uVar5) {
        if (uVar5 == *(uint *)(param_1 + 0xc4)) {
          *(uint *)(param_1 + 0xc0) = uVar5 + 1;
          *(undefined4 *)(param_1 + 0x3d8) = 1;
          return (char *)0x10c;
        }
        return (char *)-1;
      }
      local_d = **(char **)(param_1 + 0xc0);
      if (local_d != '\n') break;
      pcVar2 = *(char **)(param_1 + 0xc0) + 1;
      *(int *)(param_1 + 0x1d0) = *(int *)(param_1 + 0x1d0) + 1;
      *(char **)(param_1 + 0xc0) = pcVar2;
      *(char **)(param_1 + 0xbc) = pcVar2;
    }
    iVar3 = FUN__text__00571910((int)local_d);
    if (iVar3 == 0) break;
    *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 1;
  }
  if (local_d != '#') {
    if (local_d == ';') {
LAB__text__0053fe64:
      *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 1;
      pcVar2 = *(char **)(param_1 + 0xc0);
      if (pcVar2 < *(char **)(param_1 + 0xc4)) {
        do {
          if (*pcVar2 == '\n') break;
          pcVar2 = pcVar2 + 1;
          *(char **)(param_1 + 0xc0) = pcVar2;
        } while (pcVar2 < *(char **)(param_1 + 0xc4));
      }
    }
    else {
      if (local_d != '/') {
LAB__text__0053fec7:
        iVar8 = (int)local_d;
        iVar3 = FUN__text__005717b0(iVar8);
        if (iVar3 != 0) {
          puVar9 = *(undefined4 **)(param_1 + 0xc0);
          pcVar2 = (char *)((int)puVar9 + 1);
          *(char **)(param_1 + 0xc0) = pcVar2;
          if (pcVar2 < *(char **)(param_1 + 0xc4)) goto LAB__text__0053fef0;
          goto LAB__text__0053ff1f;
        }
        iVar3 = FUN__text__00571880(iVar8);
        pcVar2 = *(char **)(param_1 + 0xc0);
        if (iVar3 == 0) {
          if (*pcVar2 == '+') {
            *(undefined4 *)(param_1 + 0x3d8) = 1;
          }
          *(char **)(param_1 + 0xc0) = pcVar2 + 1;
          return (char *)iVar8;
        }
        pcVar4 = pcVar2 + 1;
        local_c = (char *)0x10a;
        *(char **)(param_1 + 0xc0) = pcVar4;
        if (pcVar4 < *(char **)(param_1 + 0xc4)) goto LAB__text__0053fffa;
        goto LAB__text__00540055;
      }
      pcVar4 = *(char **)(param_1 + 0xc4);
      pcVar2 = (char *)(*(int *)(param_1 + 0xc0) + 1);
      if (pcVar4 <= pcVar2) goto LAB__text__0053fec7;
      if (*pcVar2 == '/') goto LAB__text__0053fe64;
      if ((pcVar4 <= pcVar2) || (*pcVar2 != '*')) goto LAB__text__0053fec7;
      pcVar2 = (char *)(*(int *)(param_1 + 0xc0) + 2);
      *(char **)(param_1 + 0xc0) = pcVar2;
      if (pcVar2 < pcVar4) {
        do {
          pcVar2 = *(char **)(param_1 + 0xc0);
          if (((*pcVar2 == '*') && (pcVar2 + 1 < pcVar4)) && (pcVar2[1] == '/')) {
            *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 2;
            goto LAB__text__0053fe8e;
          }
          if (*pcVar2 == '\n') {
            *(int *)(param_1 + 0x1d0) = *(int *)(param_1 + 0x1d0) + 1;
            *(char **)(param_1 + 0xbc) = pcVar2 + 1;
          }
          *(char **)(param_1 + 0xc0) = pcVar2 + 1;
        } while (pcVar2 + 1 < *(char **)(param_1 + 0xc4));
      }
      pcVar2 = "comment extends past end-of-file";
LAB__text__0053fe51:
      FUN__text__0053eb92(param_1,pcVar2);
    }
    goto LAB__text__0053fe8e;
  }
  pcVar2 = *(char **)(param_1 + 0xc0);
  if (pcVar2 != *(char **)(param_1 + 0xbc)) goto LAB__text__0053fec7;
  pcVar4 = pcVar2 + 1;
  *(char **)(param_1 + 0xc0) = pcVar4;
  if (pcVar4 < *(char **)(param_1 + 0xc4)) {
    do {
      if (*pcVar4 == '\n') break;
      pcVar4 = pcVar4 + 1;
      *(char **)(param_1 + 0xc0) = pcVar4;
    } while (pcVar4 < *(char **)(param_1 + 0xc4));
  }
  local_8 = pcVar2;
  if (5 < (int)pcVar4 - (int)pcVar2) {
    iVar3 = 5;
    bVar12 = true;
    pcVar7 = pcVar2;
    pcVar10 = "#line";
    do {
      if (iVar3 == 0) break;
      iVar3 = iVar3 + -1;
      bVar12 = *pcVar7 == *pcVar10;
      pcVar7 = pcVar7 + 1;
      pcVar10 = pcVar10 + 1;
    } while (bVar12);
    if (bVar12) {
      if (pcVar2 < pcVar4) {
        do {
          iVar3 = FUN__text__00571910((int)*local_8);
          if (iVar3 != 0) break;
          local_8 = local_8 + 1;
        } while (local_8 < *(char **)(param_1 + 0xc0));
      }
      while ((pcVar2 = local_8, local_8 < *(char **)(param_1 + 0xc0) &&
             (iVar3 = FUN__text__00571910((int)*local_8), pcVar2 = local_8, iVar3 != 0))) {
        local_8 = local_8 + 1;
      }
      while ((local_8 < *(char **)(param_1 + 0xc0) &&
             (iVar3 = FUN__text__00571910((int)*local_8), iVar3 == 0))) {
        local_8 = local_8 + 1;
      }
      pcVar4 = *(char **)(param_1 + 0xc0);
      local_14 = local_8;
      if (local_8 < pcVar4) {
        do {
          if (*local_14 == '\"') break;
          local_14 = local_14 + 1;
        } while (local_14 < *(char **)(param_1 + 0xc0));
      }
      local_c = local_14;
      if ((local_14 < pcVar4) && (local_c = local_14 + 1, local_c < pcVar4)) {
        do {
          if (*local_c == '\"') break;
          local_c = local_c + 1;
        } while (local_c < *(char **)(param_1 + 0xc0));
      }
      uVar5 = (int)local_8 - (int)pcVar2;
      if (0xff < uVar5) {
        uVar5 = 0xff;
      }
      local_8 = local_c + -(int)local_14;
      if ((char *)0xff < local_c + -(int)local_14) {
        local_8 = (char *)0xff;
      }
      if (uVar5 != 0) {
        pcVar4 = local_114;
        for (uVar6 = uVar5 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
          *(undefined4 *)pcVar4 = *(undefined4 *)pcVar2;
          pcVar2 = pcVar2 + 4;
          pcVar4 = pcVar4 + 4;
        }
        for (uVar6 = uVar5 & 3; uVar6 != 0; uVar6 = uVar6 - 1) {
          *pcVar4 = *pcVar2;
          pcVar2 = pcVar2 + 1;
          pcVar4 = pcVar4 + 1;
        }
        local_114[uVar5] = '\0';
        iVar3 = FUN__text__00572840(local_114);
        *(int *)(param_1 + 0x1d0) = iVar3 + -1;
      }
      if ((char *)0x1 < local_8) {
        pcVar2 = (char *)(param_1 + 0x1d4);
        pcVar4 = local_14 + 1;
        while (pcVar4 < local_c) {
          cVar1 = *pcVar4;
          pcVar7 = pcVar4 + 1;
          *pcVar2 = cVar1;
          if (((cVar1 == '\\') && (pcVar7 < local_c)) && (*pcVar7 == '\\')) {
            pcVar7 = pcVar4 + 2;
          }
          pcVar2 = pcVar2 + 1;
          pcVar4 = pcVar7;
        }
        *pcVar2 = '\0';
      }
      goto LAB__text__0053fe8e;
    }
  }
  pcVar2 = "preprocessor directives are not supported";
  goto LAB__text__0053fe51;
  while( true ) {
    *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 1;
    pcVar2 = *(char **)(param_1 + 0xc0);
    if (*(char **)(param_1 + 0xc4) <= pcVar2) break;
LAB__text__0053fef0:
    iVar3 = FUN__text__00571990((int)*pcVar2);
    if ((iVar3 == 0) && (**(char **)(param_1 + 0xc0) != '_')) break;
  }
LAB__text__0053ff1f:
  uVar5 = *(int *)(param_1 + 0xc0) - (int)puVar9;
  if (0xff < uVar5) {
    uVar5 = 0xff;
  }
  puVar11 = (undefined4 *)(param_1 + 200);
  for (uVar6 = uVar5 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
    *puVar11 = *puVar9;
    puVar9 = puVar9 + 1;
    puVar11 = puVar11 + 1;
  }
  for (uVar6 = uVar5 & 3; uVar6 != 0; uVar6 = uVar6 - 1) {
    *(undefined1 *)puVar11 = *(undefined1 *)puVar9;
    puVar9 = (undefined4 *)((int)puVar9 + 1);
    puVar11 = (undefined4 *)((int)puVar11 + 1);
  }
  *(undefined1 *)(uVar5 + 200 + param_1) = 0;
  pcVar2 = (char *)(param_1 + 200);
  iVar3 = 3;
  bVar12 = true;
  *(undefined4 *)(param_1 + 0x3d8) = 1;
  pcVar4 = pcVar2;
  pcVar7 = "vs";
  do {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    bVar12 = *pcVar4 == *pcVar7;
    pcVar4 = pcVar4 + 1;
    pcVar7 = pcVar7 + 1;
  } while (bVar12);
  if (bVar12) {
    return (char *)0x101;
  }
  iVar3 = 3;
  bVar12 = true;
  pcVar4 = pcVar2;
  pcVar7 = "ps";
  do {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    bVar12 = *pcVar4 == *pcVar7;
    pcVar4 = pcVar4 + 1;
    pcVar7 = pcVar7 + 1;
  } while (bVar12);
  if (bVar12) {
    return (char *)0x102;
  }
  iVar3 = 4;
  bVar12 = true;
  pcVar4 = "def";
  do {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    bVar12 = *pcVar2 == *pcVar4;
    pcVar2 = pcVar2 + 1;
    pcVar4 = pcVar4 + 1;
  } while (bVar12);
  if (bVar12) {
    return (char *)0x103;
  }
  iVar3 = FUN__text__0053ecc8();
  if (iVar3 != 0x109) {
    return (char *)iVar3;
  }
  *(undefined4 *)(param_1 + 0x3d8) = 0;
  return (char *)0x109;
LAB__text__0053fffa:
  do {
    iVar3 = FUN__text__00571880((int)*pcVar4);
    if (iVar3 == 0) {
      if ((*(int *)(param_1 + 0xb4) == 0) ||
         ((**(char **)(param_1 + 0xc0) != '.' && (**(char **)(param_1 + 0xc0) != 'e')))) {
        cVar1 = **(char **)(param_1 + 0xc0);
        if (((cVar1 != '+') && (cVar1 != '-')) || ((*(char **)(param_1 + 0xc0))[-1] != 'e')) break;
      }
      local_c = (char *)0x10b;
    }
    *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 1;
    pcVar4 = *(char **)(param_1 + 0xc0);
  } while (pcVar4 < *(char **)(param_1 + 0xc4));
LAB__text__00540055:
  uVar5 = *(int *)(param_1 + 0xc0) - (int)pcVar2;
  if (0xff < uVar5) {
    uVar5 = 0xff;
  }
  pcVar4 = (char *)(param_1 + 200);
  for (uVar6 = uVar5 >> 2; uVar6 != 0; uVar6 = uVar6 - 1) {
    *(undefined4 *)pcVar4 = *(undefined4 *)pcVar2;
    pcVar2 = pcVar2 + 4;
    pcVar4 = pcVar4 + 4;
  }
  for (uVar6 = uVar5 & 3; uVar6 != 0; uVar6 = uVar6 - 1) {
    *pcVar4 = *pcVar2;
    pcVar2 = pcVar2 + 1;
    pcVar4 = pcVar4 + 1;
  }
  *(undefined1 *)(uVar5 + 200 + param_1) = 0;
  if (((*(int *)(param_1 + 0xb4) != 0) &&
      (pcVar2 = *(char **)(param_1 + 0xc0), pcVar2 < *(char **)(param_1 + 0xc4))) &&
     (*pcVar2 == 'f')) {
    local_c = (char *)0x10b;
    *(char **)(param_1 + 0xc0) = pcVar2 + 1;
  }
  return local_c;
}

