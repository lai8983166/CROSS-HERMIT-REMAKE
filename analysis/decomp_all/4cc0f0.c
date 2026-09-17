
void __thiscall FUN__text__004cc0f0(int param_1,int param_2,uint param_3,uint param_4)

{
  undefined1 uVar1;
  byte bVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  uint local_24;
  int local_20;
  undefined1 local_1c;
  uint local_18;
  int local_14;
  int local_10;
  short *local_c;
  int local_8;
  
  puVar4 = local_64;
  for (iVar3 = 0x18; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = (short *)(&DAT_00624520 + param_2 * 0x26);
  local_10 = param_1 + 0x6f60 + *local_c * 0xe0;
  local_14 = param_1 + 0x430 + *local_c * 0xab8;
  local_8 = param_1;
  uVar1 = FUN__text__004ca9b0();
  local_18 = CONCAT31(local_18._1_3_,uVar1);
  local_1c = FUN__text__004ca9e0();
  FUN__text__004caf10(0x18);
  FUN__text__004caff0(0xc);
  if (param_3 == 0xffffffff) {
    param_3 = (uint)*(short *)(local_10 + 0x34 + (local_18 & 0xff) * 2);
  }
  *(short *)(local_10 + 0x40) = *local_c * 2 + 0x16;
  *(short *)(local_10 + 0x42) = *local_c * 2 + 0x17;
  local_20 = (int)local_c[3];
  if (local_20 == 0) {
    FUN__text__004c9610(8);
    *(undefined2 *)(local_10 + 0x22) = 1;
    *(undefined2 *)(local_10 + 0x24) = 0;
  }
  else if (local_20 == 1) {
    FUN__text__004ca770(param_3 & 0xffff);
    *(short *)(local_10 + 0x2c) = local_c[5];
    *(short *)(local_10 + 0x2e) = local_c[6];
    *(short *)(local_10 + 0x30) = local_c[4];
    local_24 = (uint)*(ushort *)(local_10 + 0x22);
    switch(local_24) {
    case 0:
    case 1:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
      bVar2 = FUN__text__004ca9b0();
      local_18 = CONCAT31(local_18._1_3_,bVar2);
      if ((int)*(short *)(local_10 + 0x34 + (uint)bVar2 * 2) != param_3) {
        *(undefined2 *)(local_10 + 0x34 + (uint)bVar2 * 2) = (undefined2)param_3;
        FUN__text__004cbf90(local_10);
      }
      *(undefined2 *)(local_10 + 0x38 + (local_18 & 0xff) * 2) = (undefined2)param_4;
      break;
    case 2:
      if ((int)*(short *)(local_10 + 0x34 + (local_18 & 0xff) * 2) == param_3) {
        if (*(ushort *)(local_10 + 0x38 + (local_18 & 0xff) * 2) != param_4) {
          FUN__text__004c9610(0x14);
          *(undefined2 *)(local_10 + 0x22) = 6;
          *(undefined2 *)(local_10 + 0x24) = 0;
          *(undefined2 *)(local_10 + 0x3c + (local_18 & 0xff) * 2) =
               *(undefined2 *)(local_10 + 0x38 + (local_18 & 0xff) * 2);
          *(undefined2 *)(local_10 + 0x38 + (local_18 & 0xff) * 2) = (undefined2)param_4;
        }
      }
      else {
        FUN__text__004c9610(0x28);
        *(undefined2 *)(local_10 + 0x22) = 5;
        *(undefined2 *)(local_10 + 0x24) = 0;
        FUN__text__004caa20();
        bVar2 = FUN__text__004ca9b0();
        local_18 = CONCAT31(local_18._1_3_,bVar2);
        *(undefined2 *)(local_10 + 0x34 + (uint)bVar2 * 2) = (undefined2)param_3;
        *(undefined2 *)(local_10 + 0x38 + (uint)bVar2 * 2) = (undefined2)param_4;
        FUN__text__004cbf90(local_10);
      }
    }
  }
  local_8 = 0x4cc3bd;
  FUN__text__0056ce80();
  return;
}

