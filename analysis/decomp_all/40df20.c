
void __thiscall FUN__text__0040df20(int param_1,undefined4 *param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  int local_30;
  undefined4 *local_2c;
  undefined4 *local_28;
  undefined4 *local_24;
  undefined4 *local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  undefined4 *local_10;
  undefined4 *local_c;
  int local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  if ((*(int *)(param_1 + 0x10) != 0) && (param_3 < *(int *)(param_1 + 8))) {
    local_10 = (undefined4 *)(*(int *)(param_1 + 0x10) + param_3 * 8);
    *param_2 = *local_10;
    *local_10 = param_2;
    local_30 = param_2[1] + -1;
    local_8 = param_1;
    switch(local_30) {
    case 0:
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x5c;
      break;
    case 1:
      local_20 = param_2;
      (*API_KERNEL32_DLL_lstrlenA)(param_2 + 5);
      local_14 = FUN__text__0056ce80();
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 0x18 + local_14;
      break;
    case 2:
      local_24 = param_2;
      (*API_KERNEL32_DLL_lstrlenA)((int)param_2 + 0x11);
      local_14 = FUN__text__0056ce80();
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 0x14 + local_14;
      break;
    case 3:
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x18;
      break;
    case 4:
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x24;
      break;
    case 5:
      local_28 = param_2;
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x24;
      break;
    case 6:
      local_2c = param_2;
      if (*(byte *)((int)param_2 + 9) < 2) goto LAB__text__0040e139;
      *(uint *)(param_1 + 0x30) =
           *(int *)(param_1 + 0x30) + 0x10 + (uint)*(byte *)((int)param_2 + 9) * 4;
      break;
    case 7:
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x18;
      break;
    case 8:
      *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 0x10;
    }
    local_18 = *(int *)(local_8 + 0x14) + *(int *)(local_8 + 0xc);
    if ((local_18 <= *(uint *)(local_8 + 0x30)) &&
       (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                    DAT_005ff350 + 0x47,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_1c = *(int *)(local_8 + 0x30) - *(int *)(local_8 + 0x14);
    if (*(uint *)(local_8 + 0x1c) < local_1c) {
      *(uint *)(local_8 + 0x1c) = local_1c;
    }
  }
LAB__text__0040e139:
  local_8 = 0x40e146;
  FUN__text__0056ce80();
  return;
}

