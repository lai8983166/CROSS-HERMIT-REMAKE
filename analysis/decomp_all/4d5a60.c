
void FUN__text__004d5a60(short param_1,short param_2,short param_3,short param_4,short param_5,
                        short param_6,short param_7,short param_8,short param_9,short param_10)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  undefined2 local_28;
  undefined2 local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  uint local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = local_8 & 0xffffff00;
  local_c = param_1 + param_3 / 2;
  local_10 = param_2 + param_4 / 2;
  local_14 = param_5 + param_7 / 2 + param_9;
  local_18 = param_6 + param_8 / 2 + param_10;
  local_1c = param_7 / 2 + param_3 / 2;
  local_20 = param_8 / 2 + param_4 / 2;
  local_24 = FUN__text__0056db00((int)local_c - (int)local_14);
  local_28 = FUN__text__0056db00((int)local_10 - (int)local_18);
  local_8 = 0x4d5b62;
  FUN__text__0056ce80();
  return;
}

