
void FUN__text__0044ea80(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4
                        ,undefined4 *param_5,undefined4 param_6,undefined4 param_7)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  undefined4 local_3c;
  ushort local_38;
  ushort local_34;
  ushort local_30;
  ushort local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined1 *local_20;
  int local_1c;
  int local_18;
  int local_14;
  byte *local_10;
  byte *local_c;
  int local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = 0;
  local_14 = FUN__text__0044e6e0(param_6,param_1,CONCAT22(0xcccc,param_2));
  local_10 = (byte *)FUN__text__0044e650(param_6,local_14);
  local_18 = FUN__text__0044e6e0(param_6,param_3,CONCAT22(extraout_var,param_4));
  local_c = (byte *)FUN__text__0044e650(param_6,local_18);
  if (local_14 != local_18) {
    local_2c = (ushort)*local_10;
    local_30 = (ushort)local_10[1];
    local_34 = (ushort)*local_c;
    local_38 = (ushort)local_c[1];
    *(undefined4 *)(local_8 + 0xc) = param_6;
    FUN__text__00439c60();
    local_1c = FUN__text__004396e0();
    if (local_1c == 0) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\PathFind.cpp",
                                  DAT_00606944 + 0x25,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(ushort *)(param_5 + 6) = local_34;
      *(ushort *)((int)param_5 + 0x1a) = local_38;
    }
    else {
      local_20 = *(undefined1 **)(local_1c + 8);
      *(ushort *)(local_20 + 2) = local_2c;
      *(ushort *)(local_20 + 4) = local_30;
      *(undefined4 *)(local_20 + 0x14) = 0;
      *(undefined4 *)(local_20 + 8) = 0;
      *(int *)(local_20 + 0xc) =
           ((int)(short)local_34 - (int)(short)local_2c) *
           ((int)(short)local_34 - (int)(short)local_2c) +
           ((int)(short)local_38 - (int)(short)local_30) *
           ((int)(short)local_38 - (int)(short)local_30);
      *(int *)(local_20 + 0x10) = *(int *)(local_20 + 8) + *(int *)(local_20 + 0xc);
      *(int *)(local_20 + 0x18) = local_14;
      FUN__text__00439790();
      *local_20 = 0x40;
      FUN__text__00439a90(local_1c);
      FUN__text__004398d0((int)*(short *)(local_20 + 2),(int)*(short *)(local_20 + 4),local_1c);
      *param_5 = *(undefined4 *)(local_8 + 0x54);
      param_5[1] = *(undefined4 *)(local_8 + 0x58);
      param_5[2] = *(undefined4 *)(local_8 + 0x5c);
      param_5[3] = *(undefined4 *)(local_8 + 0x60);
      param_5[4] = *(undefined4 *)(local_8 + 100);
      param_5[5] = *(undefined4 *)(local_8 + 0x68);
      *(undefined2 *)(param_5 + 6) = param_3;
      *(undefined2 *)((int)param_5 + 0x1a) = param_4;
      *(undefined2 *)((int)param_5 + 0x1e) = (undefined2)local_14;
      *(undefined2 *)(param_5 + 8) = (undefined2)local_18;
      *(undefined1 *)((int)param_5 + 0x22) = (undefined1)param_1;
      *(undefined1 *)((int)param_5 + 0x23) = (undefined1)param_2;
      local_3c = FUN__text__0044ed40(param_5,param_7);
      local_28 = local_3c;
    }
  }
  local_8 = 0x44ed30;
  FUN__text__0056ce80();
  return;
}

