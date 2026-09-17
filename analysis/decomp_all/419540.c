
void __fastcall FUN_00419540(int param_1)

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
  if (*(int *)(param_1 + 0x134) != 0) {
    local_8 = param_1;
    (*DAT_00592270)(*(undefined4 *)(param_1 + 0x134));
    local_c = __chkesp();
    if ((local_c == 0) &&
       (iVar2 = FUN_00424f80("ret!=0","E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                             DAT_005ff564 + 6,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined4 *)(local_8 + 0x134) = 0;
  }
  local_8 = 0x4195d8;
  __chkesp();
  return;
}

