
void __fastcall FUN__text__004c7770(short *param_1)

{
  ushort uVar1;
  char cVar2;
  undefined1 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_5c [16];
  uint local_1c;
  int local_18;
  uint local_14;
  undefined4 local_10;
  short local_c;
  short *local_8;
  
  puVar5 = local_5c;
  for (iVar4 = 0x16; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_c = 1;
  if (*param_1 == 1) {
    local_1c = (uint)(ushort)param_1[1];
    local_8 = param_1;
    switch(local_1c) {
    case 0:
      local_10 = 1;
      local_14 = CONCAT31(local_14._1_3_,1);
      local_18 = CONCAT31(local_18._1_3_,0xff);
      break;
    case 1:
    case 100:
      local_10 = 2;
      local_14 = CONCAT31(local_14._1_3_,0xff);
      local_18 = CONCAT31(local_18._1_3_,0xff);
      break;
    default:
      local_c = 0;
      break;
    case 3:
      local_10 = 1;
      local_14 = CONCAT31(local_14._1_3_,1);
      cVar2 = FUN__text__004cd850(param_1[2],param_1[3],0xff);
      local_18 = CONCAT31(local_18._1_3_,-1 - cVar2);
      uVar1 = local_8[2];
      local_8[2] = local_8[2] + 1;
      if ((ushort)local_8[3] < uVar1) {
        local_8[1] = 2;
      }
      break;
    case 4:
      local_10 = 1;
      local_14 = CONCAT31(local_14._1_3_,1);
      uVar3 = FUN__text__004cd850(param_1[2],param_1[3],0xff);
      local_18 = CONCAT31(local_18._1_3_,uVar3);
      uVar1 = local_8[2];
      local_8[2] = local_8[2] + 1;
      if ((ushort)local_8[3] < uVar1) {
        local_8[1] = 0;
      }
      break;
    case 5:
      local_10 = 2;
      local_14 = CONCAT31(local_14._1_3_,0xff);
      cVar2 = FUN__text__004cd850(param_1[2],param_1[3],0xff);
      local_18 = CONCAT31(local_18._1_3_,-1 - cVar2);
      uVar1 = local_8[2];
      local_8[2] = local_8[2] + 1;
      if ((ushort)local_8[3] < uVar1) {
        local_8[1] = 2;
      }
      break;
    case 6:
      local_10 = 2;
      local_14 = CONCAT31(local_14._1_3_,0xff);
      uVar3 = FUN__text__004cd850(param_1[2],param_1[3],0xff);
      local_18 = CONCAT31(local_18._1_3_,uVar3);
      uVar1 = local_8[2];
      local_8[2] = local_8[2] + 1;
      if ((ushort)local_8[3] < uVar1) {
        local_8[1] = 100;
      }
    }
    if (local_c != 0) {
      FUN__text__00410310(0,0,0x400,0x300,0x34,
                          local_18 << 0x18 | (local_14 & 0xff) << 0x10 | (local_14 & 0xff) << 8 |
                          local_14 & 0xff,local_10);
    }
  }
  local_8 = (short *)0x4c7a1d;
  FUN__text__0056ce80();
  return;
}

