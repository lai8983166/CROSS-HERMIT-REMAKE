
/* WARNING: Removing unreachable block (ram,0x0043d731) */
/* WARNING: Removing unreachable block (ram,0x0043d754) */

void __thiscall
FUN__text__0043d660(int param_1,short param_2,short param_3,int param_4,int param_5,short *param_6,
                   short *param_7)

{
  code *pcVar1;
  short sVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar4;
  undefined4 local_88 [16];
  short local_48;
  short local_44 [10];
  int local_30;
  short local_2c;
  short local_28;
  int local_24;
  int local_20;
  undefined4 local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_88;
  for (iVar3 = 0x21; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2659c) != 0) {
    if (((param_4 < 0) || (0x20 < param_4)) &&
       (iVar3 = FUN__text__00424f80("(0<=view)&&(view<=32)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ffa1c + 7,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (0x1f < param_4) {
      param_4 = 0x20;
    }
    local_14 = (int)(char)(&DAT_0059558c)[param_4 * 2];
    local_18 = (int)(char)(&DAT_0059558d)[param_4 * 2];
    local_c = (int)param_2 - (local_14 + -1) / 2;
    local_10 = (int)param_3 - (local_18 + -1) / 2;
    local_1c = *(undefined4 *)(local_8 + 8 + param_4 * 4);
    local_30 = 5;
    local_30 = 5;
    for (local_24 = 0; local_24 != local_30; local_24 = local_24 + 1) {
      local_44[local_24] = (short)local_24;
    }
    *(short *)(local_8 + 0x263c4) = *(short *)(local_8 + 0x263c4) + 1;
    *(short *)(local_8 + 0x263c4) = *(short *)(local_8 + 0x263c4) % (short)local_30;
    for (local_24 = 0; sVar2 = local_44[0], local_24 != *(short *)(local_8 + 0x263c4) * 3;
        local_24 = local_24 + 1) {
      local_48 = local_44[0];
      local_44[0] = local_44[local_24 % local_30];
      local_44[local_24 % local_30] = sVar2;
    }
    for (local_24 = 0;
        local_24 != (int)*(short *)(local_8 + 0x263c0) * (int)*(short *)(local_8 + 0x263c2);
        local_24 = local_24 + 1) {
      local_20 = (local_24 / local_30) * local_30;
      local_20 = local_20 + local_44[local_24 % local_30];
      if ((int)(uint)*(ushort *)(*(int *)(local_8 + 0x263b8) + 2 + local_20 * 6) <= param_4) {
        local_28 = *(char *)(*(int *)(local_8 + 0x263b8) + local_20 * 6) + param_2;
        local_2c = *(char *)(*(int *)(local_8 + 0x263b8) + 1 + local_20 * 6) + param_3;
        if (((((-1 < local_28) && (local_28 < *(short *)(*(int *)(local_8 + 0x2659c) + 4))) &&
             ((-1 < local_2c && (local_2c < *(short *)(*(int *)(local_8 + 0x2659c) + 6))))) &&
            ((param_5 == 4 ||
             (iVar3 = FUN__text__0043be60((int)local_28,(int)local_2c,param_5), iVar3 != 0)))) &&
           (iVar3 = FUN__text__0043d530(local_28,local_2c), iVar3 == 0)) {
          FUN__text__0043d5b0(CONCAT22(extraout_var_00,local_28),CONCAT22(extraout_var,local_2c));
          *param_6 = local_28;
          *param_7 = local_2c;
          break;
        }
      }
    }
  }
  local_8 = 0x43d96a;
  FUN__text__0056ce80();
  return;
}

