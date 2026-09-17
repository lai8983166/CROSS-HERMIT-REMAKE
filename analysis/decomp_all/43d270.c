
void __thiscall FUN__text__0043d270(int param_1,int param_2,int param_3,int param_4)

{
  byte bVar1;
  byte bVar2;
  code *pcVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_8c [16];
  int local_4c;
  int local_48;
  uint local_44;
  byte local_40;
  undefined3 uStack_3f;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_8c;
  for (iVar4 = 0x22; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if (*(int *)(param_1 + 0x2659c) != 0) {
    local_8 = param_1;
    if (((param_4 < 0) || (0x20 < param_4)) &&
       (iVar4 = FUN__text__00424f80("(0<=view)&&(view<=32)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ffa14 + 9,0), iVar4 != 0)) {
      pcVar3 = (code *)swi(3);
      (*pcVar3)();
      return;
    }
    local_2c = (int)(char)(&DAT_0059558c)[param_4 * 2];
    local_30 = (int)(char)(&DAT_0059558d)[param_4 * 2];
    local_14 = param_2 - (local_2c + -1) / 2;
    local_18 = param_3 - (local_30 + -1) / 2;
    local_3c = *(int *)(local_8 + 8 + param_4 * 4);
    local_1c = 0;
    local_24 = 0;
    if (local_14 < 0) {
      local_1c = -local_14;
    }
    if (local_18 < 0) {
      local_24 = -local_18;
    }
    local_20 = local_2c;
    if ((int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) <= local_14 + local_2c) {
      local_20 = *(short *)(*(int *)(local_8 + 0x2659c) + 4) - local_14;
    }
    local_28 = local_30;
    if ((int)*(short *)(*(int *)(local_8 + 0x2659c) + 6) <= local_18 + local_30) {
      local_28 = local_30 -
                 ((local_18 + local_30) - (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6));
    }
    local_48 = FUN__text__0043d1a0();
    local_4c = FUN__text__0043d200();
    for (local_10 = local_24; local_10 != local_28; local_10 = local_10 + 1) {
      local_34 = (local_18 + local_10) * (int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_14
      ;
      local_38 = local_10 * local_2c;
      for (local_c = local_1c; local_c != local_20; local_c = local_c + 1) {
        bVar1 = *(byte *)(local_3c + local_38 + local_c);
        local_44 = CONCAT31(local_44._1_3_,bVar1);
        if (bVar1 != 0) {
          bVar2 = *(byte *)(local_48 + local_34 + local_c);
          _local_40 = CONCAT31(uStack_3f,bVar2);
          if (bVar2 < bVar1) {
            *(byte *)(local_48 + local_34 + local_c) = bVar1;
          }
          else {
            local_44 = CONCAT31(local_44._1_3_,bVar2);
          }
          if ((uint)*(byte *)(local_4c + local_34 + local_c) < (local_44 & 0xff)) {
            *(undefined1 *)(local_4c + local_34 + local_c) = (undefined1)local_44;
          }
        }
      }
    }
  }
  local_8 = 0x43d4d3;
  FUN__text__0056ce80();
  return;
}

