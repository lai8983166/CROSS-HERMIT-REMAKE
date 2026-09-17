
void __fastcall FUN__text__00493c40(int param_1)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 uVar4;
  undefined4 *puVar5;
  undefined4 local_58 [16];
  undefined1 local_18;
  char local_14;
  short local_10 [2];
  short local_c [2];
  int local_8;
  
  puVar5 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2a350) == 1) {
    local_c[0] = *(short *)(param_1 + 0x2a354);
    local_10[0] = *(short *)(param_1 + 0x2a356);
    FUN__text__00440e60(local_c,local_10);
  }
  else {
    if (*(int *)(param_1 + 0x2a348) != 1) goto LAB__text__00493da6;
    local_c[0] = *(short *)(param_1 + 0x2a34c);
    local_10[0] = *(short *)(param_1 + 0x2a34e);
    FUN__text__00440e60(local_c,local_10);
  }
  iVar3 = FUN__text__00456b20();
  if (iVar3 != 0) {
    if (*(char *)(*(int *)(local_8 + 0x117c38) + 0x18c) == '\0') {
      local_18 = 0xff;
    }
    else {
      local_18 = 4;
    }
    local_14 = FUN__text__0041ad60();
    iVar3 = (int)local_14;
    uVar4 = extraout_var;
    if (iVar3 == -1) {
      iVar2 = FUN__text__00424f80("myno != -1",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlFlare.cpp",
                                  DAT_0061927c + 0x16,0);
      iVar3 = 0;
      uVar4 = extraout_var_00;
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    FUN__text__00458380(local_c[0],CONCAT22(uVar4,local_10[0]),
                        CONCAT31((int3)((uint)iVar3 >> 8),local_14),local_18);
  }
  FUN__text__00493960((int)local_c[0],(int)local_10[0],
                      (int)*(char *)(*(int *)(local_8 + 0x117c38) + 0x18c));
  FUN__text__00458130(0);
LAB__text__00493da6:
  local_8 = 0x493db3;
  FUN__text__0056ce80();
  return;
}

