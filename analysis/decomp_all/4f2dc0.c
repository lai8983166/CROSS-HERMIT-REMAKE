
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004f2dc0(int param_1)

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
      FUN__text__00410310(_DAT_0075322c,_DAT_0075322e,_DAT_00753230,_DAT_00753232,_DAT_00753234,
                          (uint)*(byte *)(param_1 + 300) << 0x18,1);
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,1);
      if ((*(char *)(param_1 + 0x12a) == '\x01') || (*(char *)(param_1 + 0x12a) == '\x03')) {
        FUN__text__00410310(_UNK_00753236,_UNK_00753238,_UNK_0075323a,_UNK_0075323c,_UNK_0075323e,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_UNK_00753236,_UNK_00753238,_UNK_0075323a,_UNK_0075323c,_UNK_0075323e,
                            0xffffffff,0);
      }
    }
    if (*(char *)(local_8 + 299) == '\x01') {
      local_c = local_c & 0xffffff00;
      FUN__text__00410310(_DAT_0075322c,_DAT_0075322e,_DAT_00753230,_DAT_00753232,_DAT_00753234,
                          (uint)*(byte *)(local_8 + 0x12d) << 0x18,1);
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      if ((*(char *)(param_1 + 0x12a) == '\x01') ||
         (uVar2 = (uint)*(byte *)(param_1 + 0x12a), uVar2 == 3)) {
        local_c = CONCAT31(local_c._1_3_,2);
        while ((local_c & 0xff) < 4) {
          FUN__text__00410310(*(undefined2 *)(&DAT_0075322c + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_0075322e + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00753230 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00753232 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00753234 + (local_c & 0xff) * 10),
                              CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                                0x18) >> 0x10),0xff00) >> 8) |
                                       0xff00,0xff),1);
          local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
        }
        local_c._0_1_ = 4;
        FUN__text__00410310(_UNK_00753254,_UNK_00753256,(int)*(short *)(local_8 + 0x13a),
                            _UNK_0075325a,_UNK_0075325c,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
        local_c = CONCAT31(local_c._1_3_,5);
        FUN__text__00410310((int)*(short *)(local_8 + 0x134),_UNK_00753260,
                            (int)*(short *)(local_8 + 0x13c),_UNK_00753264,_UNK_00753266,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(local_8 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,2);
        while ((local_c & 0xff) < 4) {
          FUN__text__00410310(*(undefined2 *)(&DAT_0075322c + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_0075322e + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00753230 + (local_c & 0xff) * 10),
                              *(undefined2 *)(&DAT_00753232 + (local_c & 0xff) * 10),
                              CONCAT22((short)(uVar2 >> 0x10),
                                       *(undefined2 *)(&DAT_00753234 + (local_c & 0xff) * 10)),
                              0xffffffff,0);
          uVar2 = CONCAT31((int3)((uint)extraout_EDX >> 8),(char)local_c + '\x01');
          local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
        }
        local_c._0_1_ = 4;
        FUN__text__00410310(_UNK_00753254,_UNK_00753256,(int)*(short *)(local_8 + 0x13a),
                            _UNK_0075325a,_UNK_0075325c,0xffffffff,0);
        local_c = CONCAT31(local_c._1_3_,5);
        FUN__text__00410310((int)*(short *)(local_8 + 0x134),_UNK_00753260,
                            (int)*(short *)(local_8 + 0x13c),_UNK_00753264,
                            CONCAT22(extraout_var,_UNK_00753266),0xffffffff,0);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,6);
      if ((*(char *)(param_1 + 0x12a) == '\x01') || (*(char *)(param_1 + 0x12a) == '\x03')) {
        FUN__text__00410310(_UNK_00753268,_UNK_0075326a,_UNK_0075326c,_UNK_0075326e,_UNK_00753270,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_UNK_00753268,_UNK_0075326a,_UNK_0075326c,_UNK_0075326e,_UNK_00753270,
                            0xffffffff,0);
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = CONCAT31(local_c._1_3_,7);
      FUN__text__00410310(_UNK_00753272,_UNK_00753274,_UNK_00753276,_UNK_00753278,_UNK_0075327a,
                          CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) << 0x18)
                                                           >> 0x10),0xff00) >> 8) | 0xff00,0xff),1);
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x12a) != '\0') {
      local_c = (uint)local_c._1_3_ << 8;
      if ((*(char *)(param_1 + 0x12a) == '\x01') || (*(char *)(param_1 + 0x12a) == '\x03')) {
        FUN__text__00410310(_DAT_0075322c,_DAT_0075322e,_DAT_00753230,_DAT_00753232,_DAT_00753234,
                            CONCAT31((uint3)(CONCAT22((short)(((uint)*(byte *)(param_1 + 300) <<
                                                              0x18) >> 0x10),0xff00) >> 8) | 0xff00,
                                     0xff),1);
      }
      else {
        FUN__text__00410310(_DAT_0075322c,_DAT_0075322e,_DAT_00753230,_DAT_00753232,_DAT_00753234,
                            0xffffffff,0);
      }
    }
  }
  local_8 = 0x4f37ea;
  FUN__text__0056ce80();
  return;
}

