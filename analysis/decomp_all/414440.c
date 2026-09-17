
void __fastcall FUN__text__00414440(int param_1)

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
  if (*(int *)(param_1 + 0xb208) == 0) {
    local_8 = param_1;
    iVar2 = FUN__text__00424f80("DeskTophDC!=0",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxMain.cpp",
                                DAT_005ff538 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4144a3;
  FUN__text__0056ce80();
  return;
}

