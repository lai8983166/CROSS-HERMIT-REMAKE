
void FUN__text__0054a81a(void)

{
  int iVar1;
  undefined1 uVar2;
  int iVar3;
  int *unaff_ESI;
  
  iVar1 = unaff_ESI[0x5f];
  FUN__text__0054a5bc();
  FUN__text__0054a7ab();
  *(undefined4 *)(iVar1 + 0xc) = 0;
  uVar2 = FUN__text__0054a54b();
  *(undefined1 *)(iVar1 + 0x10) = uVar2;
  *(undefined4 *)(iVar1 + 0x14) = 0;
  *(undefined4 *)(iVar1 + 0x18) = 0;
  if ((*(char *)((int)unaff_ESI + 0x4a) == '\0') || ((char)unaff_ESI[0x10] == '\0')) {
    *(undefined1 *)(unaff_ESI + 0x16) = 0;
    *(undefined1 *)((int)unaff_ESI + 0x59) = 0;
    *(undefined1 *)((int)unaff_ESI + 0x5a) = 0;
  }
  if (*(char *)((int)unaff_ESI + 0x4a) == '\0') goto LAB__text__0054a8b8;
  if (*(char *)((int)unaff_ESI + 0x41) != '\0') {
    *(undefined4 *)(*unaff_ESI + 0x14) = 0x2e;
    (**(code **)*unaff_ESI)();
  }
  if (unaff_ESI[0x19] == 3) {
    if (unaff_ESI[0x1d] == 0) {
      if ((char)unaff_ESI[0x14] == '\0') goto LAB__text__0054a885;
      *(undefined1 *)((int)unaff_ESI + 0x5a) = 1;
    }
    else {
      *(undefined1 *)((int)unaff_ESI + 0x59) = 1;
    }
  }
  else {
    *(undefined1 *)((int)unaff_ESI + 0x59) = 0;
    *(undefined1 *)((int)unaff_ESI + 0x5a) = 0;
    unaff_ESI[0x1d] = 0;
LAB__text__0054a885:
    *(undefined1 *)(unaff_ESI + 0x16) = 1;
  }
  if ((char)unaff_ESI[0x16] != '\0') {
    FUN__text__00552c75();
    *(int *)(iVar1 + 0x14) = unaff_ESI[0x69];
  }
  if ((*(char *)((int)unaff_ESI + 0x5a) != '\0') || (*(char *)((int)unaff_ESI + 0x59) != '\0')) {
    FUN__text__00552154();
    *(int *)(iVar1 + 0x18) = unaff_ESI[0x69];
  }
LAB__text__0054a8b8:
  if (*(char *)((int)unaff_ESI + 0x41) == '\0') {
    if (*(char *)(iVar1 + 0x10) == '\0') {
      FUN__text__00550b99();
      FUN__text__005501a3();
    }
    else {
      FUN__text__00551192();
    }
    FUN__text__0054fce4();
  }
  FUN__text__0054fa49();
  if (*(char *)((int)unaff_ESI + 0xc9) == '\0') {
    if ((char)unaff_ESI[0x32] == '\0') {
      FUN__text__0054ec83();
    }
    else {
      FUN__text__0054f831();
    }
  }
  else {
    *(undefined4 *)(*unaff_ESI + 0x14) = 1;
    (**(code **)*unaff_ESI)();
  }
  FUN__text__0054e2b3();
  if (*(char *)((int)unaff_ESI + 0x41) == '\0') {
    FUN__text__0054d674();
  }
  (**(code **)(unaff_ESI[1] + 0x18))();
  (**(code **)(unaff_ESI[99] + 8))();
  if (((unaff_ESI[2] != 0) && ((char)unaff_ESI[0x10] == '\0')) &&
     (*(char *)(unaff_ESI[99] + 0x10) != '\0')) {
    iVar3 = unaff_ESI[8];
    if ((char)unaff_ESI[0x32] != '\0') {
      iVar3 = iVar3 * 3 + 2;
    }
    *(undefined4 *)(unaff_ESI[2] + 4) = 0;
    *(int *)(unaff_ESI[2] + 8) = unaff_ESI[0x46] * iVar3;
    *(undefined4 *)(unaff_ESI[2] + 0xc) = 0;
    *(uint *)(unaff_ESI[2] + 0x10) = (*(char *)((int)unaff_ESI + 0x5a) != '\0') + 2;
    *(int *)(iVar1 + 0xc) = *(int *)(iVar1 + 0xc) + 1;
  }
  return;
}

