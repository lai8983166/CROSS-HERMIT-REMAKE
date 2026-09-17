
void FUN__text__0048b720(int param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = &DAT_006c2dc8 + param_1 * 0x48;
  local_10 = FUN__text__004de8f0(param_1);
  local_18 = *(byte *)(local_10 + 3) - 1;
  switch(local_18) {
  case 0:
    local_14 = *(int *)(*(int *)(param_3 + 600) + 0x48);
    break;
  case 1:
    local_14 = (uint)*(ushort *)(local_c + 0x1c) +
               ((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (uint)*(ushort *)(local_c + 0x1e)) /
               100;
    break;
  case 2:
    local_14 = (uint)*(ushort *)(local_c + 0x1c) +
               ((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (uint)*(ushort *)(local_c + 0x1e)) /
               100;
    break;
  case 3:
    local_14 = (uint)*(ushort *)(local_c + 0x1c) +
               ((uint)*(byte *)(*(int *)(param_3 + 600) + 7) * (uint)*(ushort *)(local_c + 0x1e)) /
               100;
    break;
  case 4:
    local_14 = (uint)*(ushort *)(local_c + 0x1c) +
               ((uint)*(byte *)(*(int *)(param_3 + 600) + 8) * (uint)*(ushort *)(local_c + 0x1e)) /
               100;
    break;
  case 5:
    local_14 = (uint)*(ushort *)(local_c + 0x1c) +
               ((uint)*(byte *)(*(int *)(param_3 + 600) + 5) * (uint)*(ushort *)(local_c + 0x1e)) /
               100;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f78 + 0x1f,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x48b8e0;
  FUN__text__0056ce80();
  return;
}

