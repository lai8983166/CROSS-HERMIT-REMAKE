
void __fastcall FUN__text__0041ed00(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((*(int *)(param_1 + 4) == 0) &&
     (local_8 = param_1,
     iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                 "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexPos.cpp",
                                 DAT_005ff5c0 + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x41ed70;
  FUN__text__0056ce80();
  return;
}

