
void FUN__text__004b7fc0(short param_1,short param_2,uint param_3,undefined2 param_4,
                        undefined2 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = &DAT_0061c080;
  FUN__text__004d3050(0xd,param_5,DAT_0061c082,(int)param_1,(int)param_2,
                      (uint)DAT_0061c084 + (param_3 & 0xff) * 0x14,DAT_0061c086,DAT_0061c088,
                      DAT_0061c08a,param_4,0x80,0x80,0x80);
  local_8 = 0x4b8072;
  FUN__text__0056ce80();
  return;
}

