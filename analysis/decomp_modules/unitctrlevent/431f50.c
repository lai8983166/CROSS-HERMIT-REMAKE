
void FUN__text__00431f50(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00456b20();
  if (iVar2 != 0) {
    iVar2 = FUN__text__00424f80("tTask->IsNetwork() == 0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                DAT_005ff74c + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = 0;
  for (local_c = 0; *(short *)(param_1 + local_c * 2) != -1; local_c = local_c + 1) {
    local_14 = FUN__text__00431cc0((int)*(short *)(param_1 + local_c * 2));
    local_18 = local_8 + 0x80aec + local_14 * 0x520;
    iVar2 = FUN__text__00468d10(local_18);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0046a550(local_18);
      if (iVar2 != 0) {
        local_10 = local_10 + 1;
      }
    }
  }
  local_8 = 0x432032;
  FUN__text__0056ce80();
  return;
}

