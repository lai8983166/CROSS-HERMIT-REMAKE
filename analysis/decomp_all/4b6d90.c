
/* WARNING: Removing unreachable block (ram,0x004b6f6f) */

void __fastcall FUN__text__004b6d90(undefined4 param_1)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined4 *puVar2;
  undefined4 local_7c [16];
  uint local_3c;
  undefined2 local_38;
  undefined2 local_34;
  undefined2 local_30;
  undefined2 local_2c;
  undefined2 local_28;
  undefined2 local_24;
  undefined1 local_20 [4];
  uint local_1c;
  uint local_14;
  short local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar2 = local_7c;
  for (iVar1 = 0x1e; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = -1;
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  do {
    if (3 < (local_c & 0xffff)) {
LAB__text__004b6f69:
      local_10 = local_10 + 1;
      local_8 = 0x4b6f8e;
      FUN__text__0056ce80();
      return;
    }
    local_3c = local_c & 0xffff;
    switch(local_3c) {
    case 0:
      FUN__text__004d5ec0(local_20,0x3e2,0x25d,0x14,0x23);
      local_24 = 0x3e4;
      local_28 = 0x265;
      local_2c = 0x3d5;
      local_30 = 0x1a;
      local_34 = 0x10;
      local_38 = 0x12;
      break;
    case 1:
      FUN__text__004d5ec0(local_20,0x3e2,0x283,0x14,0x23);
      local_24 = 0x3e4;
      local_28 = 0x28e;
      local_2c = 0x3d5;
      local_30 = 0x59;
      local_34 = 0x10;
      local_38 = 0xf;
      break;
    case 2:
      FUN__text__004d5ec0(local_20,0x3e2,0x2a9,0x14,0x23);
      local_24 = 0x3e5;
      local_28 = 0x2b6;
      local_2c = 0x3d6;
      local_30 = 0x9b;
      local_34 = 0xe;
      local_38 = 0xd;
      break;
    case 3:
      FUN__text__004d5ec0(local_20,0x3e2,0x2cf,0x14,0x23);
      local_24 = 0x3e4;
      local_28 = 0x2db;
      local_2c = 0x3d5;
      local_30 = 0xd5;
      local_34 = 0xf;
      local_38 = 0x11;
    }
    if (((local_14 & 0xffff) != 0) && ((local_1c & 1) != 0)) {
      FUN__text__004db2b0(5);
      FUN__text__004d67f0(0xd,0x4c,7,CONCAT22(extraout_var,local_24),
                          CONCAT22(extraout_var_01,local_28),CONCAT22(extraout_var_00,local_2c),
                          CONCAT22(extraout_var,local_30),CONCAT22(extraout_var_01,local_34),
                          CONCAT22(extraout_var_00,local_38),4);
      local_10 = (short)local_c;
      goto LAB__text__004b6f69;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  } while( true );
}

