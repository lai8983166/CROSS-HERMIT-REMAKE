
void __thiscall FUN__text__004305c0(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  byte local_14;
  undefined *local_10;
  short *local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_3 < 0) || (0x1f < param_3)) &&
     (iVar2 = FUN__text__00424f80("(0<=eno) && (eno<32)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff72c + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((0xf < *(byte *)(*(int *)(param_2 + 600) + 0xa4)) &&
     (iVar2 = FUN__text__00424f80("(_UnitDataPlayer1P<=wk->data->player) && (wk->data->player<=_UnitDataPlayerCpu12)"
                                  ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff72c + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (short *)(local_8 + 0x2e714 + param_3 * 0x40 +
                     (uint)*(byte *)(*(int *)(param_2 + 600) + 0xa4) * 4);
  *local_c = *local_c + 1;
  iVar2 = (uint)*(ushort *)(*(int *)(param_2 + 600) + 0xc) * 0x40;
  local_10 = &DAT_006b2d88 + iVar2;
  local_18 = (byte)(&DAT_006b2d8a)[iVar2] - 1;
  switch(local_18) {
  case 0:
    local_14 = 1;
    break;
  case 1:
    local_14 = 2;
    break;
  case 2:
    local_14 = 4;
    break;
  case 3:
    local_14 = 8;
    break;
  case 4:
    local_14 = 0x10;
    break;
  default:
    local_14 = 0;
  }
  *(byte *)(local_c + 1) = *(byte *)(local_c + 1) | local_14;
  local_8 = 0x43070f;
  FUN__text__0056ce80();
  return;
}

