
void FUN__text__00551882(void)

{
  undefined4 *puVar1;
  int iVar2;
  int *unaff_EDI;
  int iStack00000004;
  
  puVar1 = (undefined4 *)(**(code **)unaff_EDI[1])();
  puVar1[1] = 0x1f;
  puVar1[5] = 0x1f;
  *puVar1 = 0;
  puVar1[2] = 0;
  puVar1[3] = 0x3f;
  puVar1[4] = 0;
  FUN__text__005512bf();
  iVar2 = FUN__text__005515f7();
  iStack00000004 = 0;
  if (0 < iVar2) {
    do {
      FUN__text__0055174a(iStack00000004);
      iStack00000004 = iStack00000004 + 1;
    } while (iStack00000004 < iVar2);
  }
  unaff_EDI[0x1c] = iVar2;
  *(undefined4 *)(*unaff_EDI + 0x14) = 0x5f;
  *(int *)(*unaff_EDI + 0x18) = iVar2;
  (**(code **)(*unaff_EDI + 4))();
  return;
}

