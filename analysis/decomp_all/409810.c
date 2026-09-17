
void __thiscall
FUN__text__00409810(int param_1,short param_2,short param_3,short param_4,short param_5,
                   undefined2 param_6,undefined4 param_7,undefined4 param_8)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x4c) == 0) &&
     (iVar2 = FUN__text__00424f80("DxSys",
                                  "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\DIRECTX\\D3dxSpFont.cpp",
                                  DAT_005ff0c8 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(local_8 + 0x4c) != 0) && (iVar2 = FUN__text__00409500(param_8), iVar2 == 0)) {
    (*API_KERNEL32_DLL_lstrlenA)(*(undefined4 *)(local_8 + 0x80));
    local_c = FUN__text__0056ce80();
    local_10 = ((int)param_4 / 2) * local_c;
    if (local_10 < param_5) {
      param_2 = param_2 + (short)((param_5 - local_10) / 2);
    }
    *(undefined2 *)(local_8 + 0x76) = param_6;
    FUN__text__00408f10((int)param_2,(int)param_3,param_7);
  }
  local_8 = 0x4098ee;
  FUN__text__0056ce80();
  return;
}

