
void __fastcall FUN__text__00428520(short *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  short local_c;
  short *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_1[3] < 1) {
    iVar2 = FUN__text__00424f80("0 < disp_cnt",
                                "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\SysListBoxCtrl.cpp",
                                DAT_005ff6cc + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = *local_8 - local_8[3];
  if (local_c < 0) {
    local_c = 0;
  }
  local_8[1] = local_8[1] + -1;
  if (local_8[1] < 0) {
    local_8[1] = 0;
    local_8[2] = local_8[2] + -1;
    if (local_8[2] < 0) {
      local_8[2] = 0;
    }
  }
  local_8 = (short *)0x4285e6;
  FUN__text__0056ce80();
  return;
}

