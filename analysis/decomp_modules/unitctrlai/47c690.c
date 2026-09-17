
void FUN__text__0047c690(int param_1,undefined4 param_2)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  uint local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00468d80(param_1);
  if ((((iVar3 == 0) && (iVar3 = FUN__text__0046a430(param_1), iVar3 == 0)) &&
      (local_10 = FUN__text__0047a8e0(param_1), *(char *)(local_10 + 0x19) != '\0')) &&
     (*(char *)(local_10 + 0x1a) != '\0')) {
    if (((*(char *)(local_10 + 0x1a) < '\x01') || ('1' < *(char *)(local_10 + 0x1a))) &&
       (iVar3 = FUN__text__00424f80("(1<=aiw->attack_skill) && (aiw->attack_skill<50)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e5c + 0x11,0), iVar3 != 0)) {
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
    local_c = &DAT_00738808 + *(char *)(local_10 + 0x1a) * 8;
    if (*(short *)(*(int *)(param_1 + 600) + 0x84) != 0) {
      local_18 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                     DAT_00618e5c + 0x16);
      local_18 = local_18 % 100;
      local_1c = (int)*local_c;
      for (local_14 = 0; local_14 != 8; local_14 = local_14 + 1) {
        if ((*(ushort *)(*(int *)(param_1 + 600) + 0x84 + local_14 * 2) & 0x8000) == 0) {
          uVar1 = *(ushort *)(*(int *)(param_1 + 600) + 0x84 + local_14 * 2);
          local_20 = uVar1 & 0x7fff;
          if ((uVar1 & 0x7fff) == 0) goto LAB__text__0047c881;
          if ((local_18 < local_1c) && (iVar3 = FUN__text__0046c930(param_1,local_20), iVar3 != 0))
          break;
          if (local_14 != 7) {
            local_1c = local_1c + local_c[local_14 + 1];
          }
        }
      }
      if (local_14 != 8) {
        FUN__text__0047c8a0(param_1,param_2,
                            *(undefined2 *)(*(int *)(param_1 + 600) + 0x84 + local_14 * 2));
      }
    }
  }
LAB__text__0047c881:
  local_8 = 0x47c88e;
  FUN__text__0056ce80();
  return;
}

