
void __fastcall FUN__text__00417650(int param_1)

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
  for (local_c = 0; local_c != 100; local_c = local_c + 1) {
    if (*(int *)(param_1 + local_c * 8) == 0) goto LAB__text__004176c8;
  }
  local_8 = param_1;
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DxPalTbl.cpp",
                              DAT_005ff550 + 6,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__004176c8:
  local_8 = 0x4176d5;
  FUN__text__0056ce80();
  return;
}

