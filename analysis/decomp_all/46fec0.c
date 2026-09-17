
void FUN__text__0046fec0(short param_1,short param_2,short param_3,short param_4,short param_5,
                        short param_6,short param_7,short param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  short local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0056db00((int)param_1 - (int)param_3);
  local_1c = (short)(iVar1 / 2);
  iVar1 = FUN__text__0056db00((int)param_2 - (int)param_4);
  local_20 = (short)(iVar1 / 2);
  local_c = param_1 + local_1c;
  local_10 = param_2 + local_20;
  iVar1 = FUN__text__0056db00((int)param_5 - (int)param_7);
  local_24 = (short)(iVar1 / 2);
  iVar1 = FUN__text__0056db00((int)param_6 - (int)param_8);
  local_28 = (short)(iVar1 / 2);
  local_14 = param_5 + local_24;
  local_18 = param_6 + local_28;
  iVar1 = FUN__text__0056db00((int)local_14 - (int)local_c);
  if (iVar1 <= (int)local_1c + (int)local_24) {
    FUN__text__0056db00((int)local_18 - (int)local_10);
  }
  local_8 = 0x46ffdd;
  FUN__text__0056ce80();
  return;
}

