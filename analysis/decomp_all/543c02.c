
void FUN__text__00543c02(int param_1,int param_2,int param_3)

{
  int *piVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  int iVar5;
  char *pcVar6;
  bool bVar7;
  
  iVar3 = param_1;
  if ((*(byte *)(param_1 + 0x5c) & 0x40) == 0) {
    FUN__text__0054c42d(param_1);
  }
  if ((*(char *)(iVar3 + 0x113) != '\0') && ((*(byte *)(iVar3 + 0x60) & 2) != 0)) {
    cVar2 = *(char *)(iVar3 + 0x114);
    if (cVar2 == '\0') {
      if ((*(byte *)(iVar3 + 0xd4) & 7) != 0) {
        bVar7 = param_3 == 0;
LAB__text__00543d14:
        if (bVar7) goto LAB__text__00543c6a;
        uVar4 = 0xff;
LAB__text__00543d1f:
        FUN__text__0054bdd3(iVar3,param_3,uVar4);
LAB__text__00543c6a:
        FUN__text__0054cdba(iVar3);
        return;
      }
    }
    else if (cVar2 == '\x01') {
      if (((*(byte *)(iVar3 + 0xd4) & 7) != 0) || (*(uint *)(iVar3 + 0xb8) < 5)) {
        if (param_3 == 0) goto LAB__text__00543c6a;
        uVar4 = 0xf;
        goto LAB__text__00543d1f;
      }
    }
    else if (cVar2 == '\x02') {
      if (((byte)*(uint *)(iVar3 + 0xd4) & 7) != 4) {
        if (param_3 == 0) goto LAB__text__00543c6a;
        bVar7 = (*(uint *)(iVar3 + 0xd4) & 4) == 0;
        goto LAB__text__00543d14;
      }
    }
    else if (cVar2 == '\x03') {
      if (((*(byte *)(iVar3 + 0xd4) & 3) != 0) || (*(uint *)(iVar3 + 0xb8) < 3)) {
        if (param_3 == 0) goto LAB__text__00543c6a;
        uVar4 = 0x33;
        goto LAB__text__00543d1f;
      }
    }
    else if (cVar2 == '\x04') {
      if (((byte)*(uint *)(iVar3 + 0xd4) & 3) != 2) {
        if (param_3 == 0) goto LAB__text__00543c6a;
        bVar7 = (*(uint *)(iVar3 + 0xd4) & 2) == 0;
        goto LAB__text__00543d14;
      }
    }
    else if (cVar2 == '\x05') {
      if (((*(byte *)(iVar3 + 0xd4) & 1) != 0) || (*(uint *)(iVar3 + 0xb8) < 2)) {
        if (param_3 == 0) goto LAB__text__00543c6a;
        uVar4 = 0x55;
        goto LAB__text__00543d1f;
      }
    }
    else if ((cVar2 == '\x06') && ((*(byte *)(iVar3 + 0xd4) & 1) == 0)) goto LAB__text__00543c6a;
  }
  if ((*(byte *)(iVar3 + 0x58) & 4) == 0) {
    FUN__text__0054381d(iVar3,"Invalid attempt to read row data");
  }
  *(undefined4 *)(iVar3 + 0x70) = *(undefined4 *)(iVar3 + 0xdc);
  *(undefined4 *)(iVar3 + 0x74) = *(undefined4 *)(iVar3 + 0xcc);
  do {
    if (*(int *)(iVar3 + 0x68) == 0) {
      if (*(int *)(iVar3 + 0xfc) == 0) {
        do {
          FUN__text__0054c5c9(iVar3,0);
          FUN__text__00546578(iVar3,&param_1,4);
          uVar4 = FUN__text__0054bcc3(&param_1);
          *(undefined4 *)(iVar3 + 0xfc) = uVar4;
          FUN__text__005466ca(iVar3);
          FUN__text__0054bcf9(iVar3,(int *)(iVar3 + 0x10c),4);
          if (*(int *)(iVar3 + 0x10c) != DAT_005d2c1c) {
            FUN__text__0054381d(iVar3,"Not enough image data");
          }
        } while (*(int *)(iVar3 + 0xfc) == 0);
      }
      *(uint *)(iVar3 + 0x68) = *(uint *)(iVar3 + 0xa0);
      *(undefined4 *)(iVar3 + 100) = *(undefined4 *)(iVar3 + 0x9c);
      if (*(uint *)(iVar3 + 0xfc) < *(uint *)(iVar3 + 0xa0)) {
        *(uint *)(iVar3 + 0x68) = *(uint *)(iVar3 + 0xfc);
      }
      FUN__text__0054bcf9(iVar3,*(undefined4 *)(iVar3 + 0x9c),*(undefined4 *)(iVar3 + 0x68));
      *(int *)(iVar3 + 0xfc) = *(int *)(iVar3 + 0xfc) - *(int *)(iVar3 + 0x68);
    }
    iVar5 = FUN__text__0054b721((undefined4 *)(iVar3 + 100),1);
    if (iVar5 == 1) {
      if (((*(int *)(iVar3 + 0x74) != 0) || (*(int *)(iVar3 + 0x68) != 0)) ||
         (*(int *)(iVar3 + 0xfc) != 0)) {
        FUN__text__0054381d(iVar3,"Extra compressed data");
      }
      *(uint *)(iVar3 + 0x58) = *(uint *)(iVar3 + 0x58) | 8;
      *(uint *)(iVar3 + 0x5c) = *(uint *)(iVar3 + 0x5c) | 0x20;
      break;
    }
    if (iVar5 != 0) {
      pcVar6 = *(char **)(iVar3 + 0x7c);
      if (pcVar6 == (char *)0x0) {
        pcVar6 = "Decompression error";
      }
      FUN__text__0054381d(iVar3,pcVar6);
    }
  } while (*(int *)(iVar3 + 0x74) != 0);
  *(undefined1 *)(iVar3 + 0xfa) = *(undefined1 *)(iVar3 + 0x11a);
  *(undefined1 *)(iVar3 + 0xf9) = *(undefined1 *)(iVar3 + 0x117);
  *(byte *)(iVar3 + 0xfb) = *(byte *)(iVar3 + 0x119);
  *(undefined1 *)(iVar3 + 0xf8) = *(undefined1 *)(iVar3 + 0x116);
  piVar1 = (int *)(iVar3 + 0xf0);
  *piVar1 = *(int *)(iVar3 + 0xd0);
  *(uint *)(iVar3 + 0xf4) = (uint)*(byte *)(iVar3 + 0x119) * *(int *)(iVar3 + 0xd0) + 7 >> 3;
  FUN__text__0054c2b2(iVar3,piVar1,*(undefined1 **)(iVar3 + 0xdc) + 1,*(int *)(iVar3 + 0xd8) + 1,
                      **(undefined1 **)(iVar3 + 0xdc));
  FUN__text__0054bc6f(iVar3,*(undefined4 *)(iVar3 + 0xd8),*(undefined4 *)(iVar3 + 0xdc),
                      *(int *)(iVar3 + 200) + 1);
  if (*(int *)(iVar3 + 0x60) != 0) {
    FUN__text__00546232(iVar3);
  }
  if ((*(char *)(iVar3 + 0x113) == '\0') || ((*(uint *)(iVar3 + 0x60) & 2) == 0)) {
    if (param_2 != 0) {
      FUN__text__0054bdd3(iVar3,param_2,0xff);
    }
    if (param_3 == 0) goto LAB__text__00543f7f;
    uVar4 = 0xff;
    iVar5 = param_3;
  }
  else {
    if (*(byte *)(iVar3 + 0x114) < 6) {
      FUN__text__0054bfe9(piVar1,*(int *)(iVar3 + 0xdc) + 1,*(byte *)(iVar3 + 0x114),
                          *(uint *)(iVar3 + 0x60));
    }
    if (param_3 != 0) {
      FUN__text__0054bdd3(iVar3,param_3,
                          *(undefined4 *)(&DAT_005d2bf8 + (uint)*(byte *)(iVar3 + 0x114) * 4));
    }
    if (param_2 == 0) goto LAB__text__00543f7f;
    uVar4 = *(undefined4 *)(&DAT_005d2bdc + (uint)*(byte *)(iVar3 + 0x114) * 4);
    iVar5 = param_2;
  }
  FUN__text__0054bdd3(iVar3,iVar5,uVar4);
LAB__text__00543f7f:
  FUN__text__0054cdba(iVar3);
  if (*(code **)(iVar3 + 0x16c) != (code *)0x0) {
    (**(code **)(iVar3 + 0x16c))(iVar3,*(undefined4 *)(iVar3 + 0xd4),*(undefined1 *)(iVar3 + 0x114))
    ;
  }
  return;
}

