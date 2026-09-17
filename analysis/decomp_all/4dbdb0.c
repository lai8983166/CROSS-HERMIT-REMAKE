
void FUN__text__004dbdb0(int param_1,undefined2 *param_2)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_94 [16];
  int local_54;
  uint local_50;
  int local_4c;
  int local_48;
  uint local_44;
  int local_40;
  int local_3c;
  uint local_38;
  int local_34;
  int local_30;
  uint local_2c;
  int local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  uint local_14;
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar3 = local_94;
  for (iVar2 = 0x24; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_006c32d8;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_14 = (uint)*(byte *)(param_1 + 0x1c);
  local_18 = (int)*(short *)(local_8 + 0x22);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *param_2 = uVar1;
  local_1c = (int)*(short *)(local_8 + 0x24);
  local_20 = (uint)*(byte *)(param_1 + 0x1c);
  local_24 = (int)*(short *)(local_8 + 0x26);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  param_2[1] = uVar1;
  local_28 = (int)*(short *)(local_8 + 0x28);
  local_2c = (uint)*(byte *)(param_1 + 0x1c);
  local_30 = (int)*(short *)(local_8 + 0x2a);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  param_2[2] = uVar1;
  local_34 = (int)*(short *)(local_8 + 0x2c);
  local_38 = (uint)*(byte *)(param_1 + 0x1c);
  local_3c = (int)*(short *)(local_8 + 0x2e);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  param_2[5] = uVar1;
  local_40 = (int)*(short *)(local_8 + 0x30);
  local_44 = (uint)*(byte *)(param_1 + 0x1c);
  local_48 = (int)*(short *)(local_8 + 0x32);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  param_2[4] = uVar1;
  local_4c = (int)*(short *)(local_8 + 0x34);
  local_50 = (uint)*(byte *)(param_1 + 0x1c);
  local_54 = (int)*(short *)(local_8 + 0x36);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  param_2[3] = uVar1;
  local_8 = (undefined *)0x4dbff2;
  FUN__text__0056ce80();
  return;
}

