
void FUN__text__0046fff0(short param_1,short param_2,short param_3,undefined4 param_4,short param_5,
                        short param_6,short param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0056db00((int)param_5 - (int)param_1);
  if (iVar1 <= (int)param_3 + (int)param_7) {
    FUN__text__0056db00((int)param_6 - (int)param_2);
  }
  local_8 = 0x470065;
  FUN__text__0056ce80();
  return;
}

