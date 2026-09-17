
void FUN__text__0047a240(int param_1)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_78 [16];
  char local_38;
  short local_34;
  short local_30;
  int local_2c;
  int local_28;
  uint local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  char *local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_78;
  for (iVar3 = 0x1d; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                              DAT_00618e28 + 10,0);
  if (iVar3 == 0) {
    local_38 = *local_10;
    if (local_38 == '\0') {
      iVar3 = FUN__text__0046a430(param_1);
      if (iVar3 == 0) {
        local_24 = (uint)local_24._1_3_ << 8;
      }
      else {
        local_24 = CONCAT31(local_24._1_3_,1);
      }
      local_14 = *(int *)(param_1 + 0x2ec) >> 0x10;
      local_18 = *(int *)(param_1 + 0x2f0) >> 0x10;
      local_34 = -1;
      local_2c = 0x7fffffff;
      for (local_30 = 0; local_30 != 0xfa; local_30 = local_30 + 1) {
        iVar3 = FUN__text__00468d10(local_8 + 0x80aec + local_30 * 0x520);
        if ((iVar3 != 0) &&
           (uVar2 = FUN__text__0046a430(local_8 + 0x80aec + local_30 * 0x520),
           uVar2 == (local_24 & 0xff))) {
          local_1c = *(int *)(local_8 + 0x80dd8 + local_30 * 0x520) >> 0x10;
          local_20 = *(int *)(local_8 + 0x80ddc + local_30 * 0x520) >> 0x10;
          local_28 = (local_14 - local_1c) * (local_14 - local_1c) +
                     (local_18 - local_20) * (local_18 - local_20);
          if (local_28 < local_2c) {
            local_34 = local_30;
            local_2c = local_28;
          }
        }
      }
      if (local_34 != -1) {
        *(short *)(param_1 + 0x4ee) = local_34;
        *(short *)(param_1 + 0x4d0) =
             (short)((uint)*(undefined4 *)(local_8 + 0x80dd8 + *(short *)(param_1 + 0x4ee) * 0x520)
                    >> 0x10);
        *(short *)(param_1 + 0x4d2) =
             (short)((uint)*(undefined4 *)(local_8 + 0x80ddc + *(short *)(param_1 + 0x4ee) * 0x520)
                    >> 0x10);
        FUN__text__00475270(param_1,6);
      }
    }
    local_8 = 0x47a460;
    FUN__text__0056ce80();
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

