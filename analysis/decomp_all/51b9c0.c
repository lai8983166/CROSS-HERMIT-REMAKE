
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__0051b9c0(int param_1)

{
  int iVar1;
  undefined2 extraout_var;
  uint uVar2;
  undefined4 extraout_EDX;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = *(byte *)(param_1 + 0x37) - 1;
  local_8 = param_1;
  switch(local_10) {
  case 0:
    if (*(char *)(param_1 + 0x12a) == '\x01') {
      local_c = local_c & 0xffffff00;
      FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                          (uint)*(byte *)(param_1 + 300) << 0x18,1);
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,1);
      if ((*(char *)(param_1 + 0x12a) == '\x01') || (*(char *)(param_1 + 0x12a) == '\x03')) {
        FUN__text__00410310(_UNK_0075882a,_UNK_0075882c,_UNK_0075882e,_UNK_00758830,_UNK_00758832,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_UNK_0075882a,_UNK_0075882c,_UNK_0075882e,_UNK_00758830,_UNK_00758832,
                            0xffffffff,0);
      }
    }
    if (*(char *)(local_8 + 299) == '\x01') {
      local_c = local_c & 0xffffff00;
      FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                          (uint)*(byte *)(local_8 + 0x12d) << 0x18,1);
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      if ((*(char *)(param_1 + 0x12a) == '\x01') ||
         (uVar2 = (uint)*(byte *)(param_1 + 0x12a), uVar2 == 3)) {
        local_c = CONCAT31(local_c._1_3_,2);
        while ((local_c & 0xff) < 4) {
          FUN__text__00410310(*(undefined2 *)(&DAT_00758820 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758822 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758824 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758826 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758828 + (local_c & 0xff) * 10),
                              CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                                0x18) >> 0x10),0xff00) >> 8) |
                                       0xff00,0xff),1);
          local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
        }
        local_c._0_1_ = 4;
        FUN__text__00410310(_UNK_00758848,_UNK_0075884a,(int)*(short *)(local_8 + 0x13a),
                            _UNK_0075884e,_UNK_00758850,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
        local_c = CONCAT31(local_c._1_3_,5);
        FUN__text__00410310((int)*(short *)(local_8 + 0x134),_UNK_00758854,
                            (int)*(short *)(local_8 + 0x13c),_UNK_00758858,_UNK_0075885a,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,2);
        while ((local_c & 0xff) < 4) {
          FUN__text__00410310(*(undefined2 *)(&DAT_00758820 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758822 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758824 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00758826 + (local_c & 0xff) * 10),
                              CONCAT22((short)(uVar2 >> 0x10),
                                       *(undefined2 *)(&DAT_00758828 + (local_c & 0xff) * 10)),
                              0xffffffff,0);
          uVar2 = CONCAT31((int3)((uint)extraout_EDX >> 8),(char)local_c + '\x01');
          local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
        }
        local_c._0_1_ = 4;
        FUN__text__00410310(_UNK_00758848,_UNK_0075884a,(int)*(short *)(local_8 + 0x13a),
                            _UNK_0075884e,_UNK_00758850,0xffffffff,0);
        local_c = CONCAT31(local_c._1_3_,5);
        FUN__text__00410310((int)*(short *)(local_8 + 0x134),_UNK_00758854,
                            (int)*(short *)(local_8 + 0x13c),_UNK_00758858,
                            CONCAT22(extraout_var,_UNK_0075885a),0xffffffff,0);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,6);
      if ((*(char *)(param_1 + 0x12a) == '\x01') || (*(char *)(param_1 + 0x12a) == '\x03')) {
        FUN__text__00410310(_UNK_0075885c,_UNK_0075885e,_UNK_00758860,_UNK_00758862,_UNK_00758864,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_UNK_0075885c,_UNK_0075885e,_UNK_00758860,_UNK_00758862,_UNK_00758864,
                            0xffffffff,0);
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,7);
      FUN__text__00410310(_UNK_00758866,_UNK_00758868,_UNK_0075886a,_UNK_0075886c,_UNK_0075886e,
                          CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) << 0x18)
                                                           >> 0x10),0xff00) >> 8) | 0xff00,0xff),1);
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = (uint)local_c._1_3_ << 8;
      FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                          (uint)*(byte *)(param_1 + 300) << 0x18,1);
    }
    if (*(char *)(local_8 + 299) != '\0') {
      local_c = CONCAT31(local_c._1_3_,8);
      FUN__text__00410310(_DAT_00758870,_UNK_00758872,_UNK_00758874,_UNK_00758876,_UNK_00758878,
                          (uint)*(byte *)(local_8 + 0x12d) << 0x18,1);
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = (uint)local_c._1_3_ << 8;
      FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                          (uint)*(byte *)(param_1 + 300) << 0x18,1);
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = (uint)local_c._1_3_ << 8;
      FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                          (uint)*(byte *)(param_1 + 300) << 0x18,1);
    }
    if (*(char *)(local_8 + 299) != '\0') {
      local_c = local_c & 0xffffff00;
      if ((*(char *)(local_8 + 299) == '\x01') || (*(char *)(local_8 + 299) == '\x03')) {
        FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 0x12d) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_DAT_00758820,_DAT_00758822,_DAT_00758824,_DAT_00758826,_DAT_00758828,
                            0xffffffff,0);
      }
    }
  }
  local_8 = 0x51c69a;
  FUN__text__0056ce80();
  return;
}

