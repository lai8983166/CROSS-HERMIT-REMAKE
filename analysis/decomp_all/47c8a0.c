
void FUN__text__0047c8a0(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  uint local_28;
  byte local_24;
  undefined2 local_20;
  undefined2 local_1c;
  int local_18;
  undefined4 local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar4 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = &DAT_006c2dc8 + param_3 * 0x48;
  local_10 = &DAT_006b2d88 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  local_14 = FUN__text__0047a8e0(param_1);
  iVar3 = FUN__text__0046abc0(param_1,param_2);
  if ((((iVar3 == 0) && (iVar3 = FUN__text__0046ad60(param_1,param_2), iVar3 == 0)) ||
      (local_18 = (*(short *)(*(int *)(param_2 + 600) + 0x16) * 100) /
                  (int)*(short *)(*(int *)(param_2 + 600) + 0x14), 0x31 < local_18)) ||
     (*(short *)(local_c + 2) == 5)) {
    local_24 = local_c[0x19];
    if (local_24 == 0) {
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e60 + 0x19,0);
      if (iVar3 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    else if ((2 < local_24) && (local_24 < 5)) {
      *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(param_1 + 2);
      *(undefined2 *)(param_1 + 0x4f2) = (undefined2)param_3;
      *(char *)(param_1 + 0x4f0) =
           (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                       (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      *(char *)(param_1 + 0x4f1) =
           (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                       (*(int *)(param_1 + 0x2f0) >> 0x1f & 0x1fU)) >> 5);
      goto switchD__text__0047ca5c_default;
    }
    iVar3 = (int)((*(int *)(param_2 + 0x2ec) >> 0x10) + (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU))
            >> 5;
    local_1c = (undefined2)iVar3;
    iVar2 = (int)((*(int *)(param_2 + 0x2f0) >> 0x10) + (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU))
            >> 4;
    local_20 = (undefined2)iVar2;
    local_28 = (uint)(byte)local_c[0x18];
    switch(local_28) {
    case 0:
    case 5:
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e60 + 0x2e,0);
      if (iVar3 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 1:
    case 2:
    case 3:
    case 4:
      *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(param_2 + 2);
      *(undefined2 *)(param_1 + 0x4f2) = (undefined2)param_3;
      local_1c._0_1_ = (undefined1)iVar3;
      *(undefined1 *)(param_1 + 0x4f0) = (undefined1)local_1c;
      local_20._0_1_ = (undefined1)iVar2;
      *(undefined1 *)(param_1 + 0x4f1) = (undefined1)local_20;
      break;
    case 6:
      *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(param_1 + 2);
      *(undefined2 *)(param_1 + 0x4f2) = (undefined2)param_3;
      *(char *)(param_1 + 0x4f0) =
           (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                       (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      *(char *)(param_1 + 0x4f1) =
           (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                       (*(int *)(param_1 + 0x2f0) >> 0x1f & 0x1fU)) >> 5);
    }
  }
switchD__text__0047ca5c_default:
  local_8 = 0x47cb3b;
  FUN__text__0056ce80();
  return;
}

