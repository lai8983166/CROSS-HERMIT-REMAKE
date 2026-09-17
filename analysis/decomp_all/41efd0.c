
void FUN__text__0041efd0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                              DAT_005ff5cc + 3,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  for (local_c = 0; local_c != 0x100; local_c = local_c + 1) {
    if (*(int *)(local_8 + local_c * 8) == 0) goto LAB__text__0041f078;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                              DAT_005ff5cc + 7,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__0041f078:
  local_8 = 0x41f085;
  FUN__text__0056ce80();
  return;
}

