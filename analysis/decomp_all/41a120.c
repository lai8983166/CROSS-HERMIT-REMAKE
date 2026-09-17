
void __thiscall FUN__text__0041a120(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = param_2;
  if (param_2 == 1) {
    local_10 = 0xffffffff;
  }
  else {
    local_10 = 0;
  }
  local_8 = param_1;
  (*API_KERNEL32_DLL_WaitForSingleObject)(*(undefined4 *)(param_1 + 0x134),local_10);
  local_18 = FUN__text__0056ce80();
  local_c = local_18;
  if (((local_18 != 0) && (local_18 != 0x102)) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff57c + 0x16,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = 0x41a1d6;
  FUN__text__0056ce80();
  return;
}

