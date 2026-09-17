
void FUN__text__004c7190(void)

{
  undefined1 uVar1;
  short sVar2;
  uint uVar3;
  int iVar4;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 uVar5;
  undefined4 *puVar6;
  undefined4 local_70 [16];
  int local_30;
  short local_2c;
  undefined2 local_28;
  uint local_24;
  uint local_20;
  int local_1c;
  int local_18;
  undefined1 local_14;
  undefined3 uStack_13;
  undefined1 local_10;
  undefined3 uStack_f;
  undefined1 local_c;
  byte *local_8;
  
  iVar4 = 0x1b;
  puVar6 = local_70;
  while( true ) {
    if (iVar4 == 0) break;
    iVar4 = iVar4 + -1;
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  uVar1 = FUN__text__004c7070();
  _local_10 = CONCAT31(uStack_f,uVar1);
  uVar1 = FUN__text__004c70a0();
  _local_14 = CONCAT31(uStack_13,uVar1);
  local_18 = (uint)*local_8 * 2 + 0x4a;
  local_1c = (uint)*local_8 * 2 + 0x4b;
  sVar2 = ((ushort)_local_10 & 0xff) + 0x30 + (ushort)*local_8 * 2;
  local_20 = CONCAT22(local_20._2_2_,sVar2);
  local_24 = CONCAT22(local_24._2_2_,((ushort)_local_14 & 0xff) + 0x30 + (ushort)*local_8 * 2);
  local_28 = 0;
  local_2c = 0;
  local_30 = local_8[8] - 1;
  uVar5 = (undefined2)((uint)local_30 >> 0x10);
  switch(local_30) {
  case 0:
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,0xffffffff,0xffffffff,local_18,0,sVar2,0);
    break;
  case 1:
    local_28 = FUN__text__004cd850(*(undefined2 *)(local_8 + 10),
                                   CONCAT22(uVar5,*(undefined2 *)(local_8 + 0xc)),0xff);
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,CONCAT22(extraout_var,local_28),0xffffffff,local_18,0,
                                  local_20 & 0xffff,0);
    *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
    if (*(ushort *)(local_8 + 0xc) < *(ushort *)(local_8 + 10)) {
      local_8[10] = 0;
      local_8[0xb] = 0;
      local_8[8] = 1;
    }
    break;
  case 2:
    uVar3 = FUN__text__004cd850(*(undefined2 *)(local_8 + 10),
                                CONCAT22(uVar5,*(undefined2 *)(local_8 + 0xc)),0xff);
    iVar4 = 0xff - (uVar3 & 0xffff);
    local_28 = (undefined2)iVar4;
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,iVar4,0xffffffff,local_18,0,local_20 & 0xffff,0);
    *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
    if (*(ushort *)(local_8 + 0xc) < *(ushort *)(local_8 + 10)) {
      local_8[10] = 0;
      local_8[0xb] = 0;
      local_8[8] = 0;
    }
    break;
  case 3:
    uVar3 = FUN__text__004cd850(*(undefined2 *)(local_8 + 10),*(undefined2 *)(local_8 + 0xc),0x7f);
    iVar4 = 0xff - (uVar3 & 0xffff);
    local_2c = (short)iVar4;
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,0xff,iVar4,local_18,0,local_20 & 0xffff,0);
    *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
    if (*(ushort *)(local_8 + 0xc) < *(ushort *)(local_8 + 10)) {
      local_8[10] = 0;
      local_8[0xb] = 0;
      local_8[8] = 1;
    }
    break;
  case 4:
    local_2c = FUN__text__004cd850(*(undefined2 *)(local_8 + 10),
                                   CONCAT22(uVar5,*(undefined2 *)(local_8 + 0xc)),0x7f);
    local_2c = local_2c + 0x80;
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,0xff,CONCAT22(extraout_var_00,local_2c),local_18,0,
                                  local_20 & 0xffff,0);
    *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
    if (*(ushort *)(local_8 + 0xc) < *(ushort *)(local_8 + 10)) {
      local_8[10] = 0;
      local_8[0xb] = 0;
      local_8[8] = 0;
    }
    break;
  case 5:
    local_28 = FUN__text__004cd850(*(undefined2 *)(local_8 + 10),
                                   CONCAT22(uVar5,*(undefined2 *)(local_8 + 0xc)),0xff);
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,CONCAT22(extraout_var_01,local_28),0xffffffff,local_18,0,
                                  local_20 & 0xffff,0);
    local_c = FUN__text__004cbca0((int)*(short *)(local_8 + 4),(int)*(short *)(local_8 + 6),0,100,
                                  100,0xff,0xffffffff,local_1c,0,local_24 & 0xffff,0);
    *(short *)(local_8 + 10) = *(short *)(local_8 + 10) + 1;
    if (*(ushort *)(local_8 + 0xc) < *(ushort *)(local_8 + 10)) {
      local_8[10] = 0;
      local_8[0xb] = 0;
      local_8[8] = 1;
    }
  }
  local_8 = (byte *)0x4c762a;
  FUN__text__0056ce80();
  return;
}

