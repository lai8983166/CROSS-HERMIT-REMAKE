
/* WARNING: Removing unreachable block (ram,0x004c8f9b) */

void __thiscall FUN__text__004c8f60(int *param_1,int param_2)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_284 [16];
  undefined1 local_244 [256];
  short local_144;
  uint local_140;
  short local_13c;
  short local_138;
  short local_134;
  short local_130;
  undefined1 local_12c [4];
  uint local_128;
  uint local_120;
  uint *local_11c;
  uint local_118;
  uint local_114;
  uint local_10;
  undefined1 local_c;
  int *local_8;
  
  puVar2 = local_284;
  for (iVar1 = 0xa0; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = CONCAT22(local_10._2_2_,1);
  local_c = 0;
  local_118 = CONCAT22(local_118._2_2_,*(undefined2 *)(*param_1 + 4));
  local_11c = DAT_007e0e5c;
  local_144 = 0;
  local_114 = local_114 & 0xffff0000;
  local_8 = param_1;
  do {
    if ((local_118 & 0xffff) <= (local_114 & 0xffff)) {
      FUN__text__004d5bf0(0);
      FUN__text__004d5d10(local_12c);
      if (((*(char *)((int)local_8 + 0x16) == '\0') || (local_144 != 0)) || ((local_128 & 1) == 0))
      {
        if ((*(char *)((int)local_8 + 0x15) != '\0') && ((local_128 & 2) != 0)) {
          *(undefined2 *)(&DAT_007d7c4c + param_2 * 0x1c8) = 0;
          *(int *)(&DAT_007d7c44 + param_2 * 0x1c8) = local_8[3];
          if ((char)local_8[5] == '\x01') {
            FUN__text__004c1f40(param_2,(uint)local_8[2] >> 0x1c,local_8[2] & 0xfffffff,0xffffffff);
          }
        }
      }
      else {
        *(undefined2 *)(&DAT_007d7c4c + param_2 * 0x1c8) = 0;
        *(int *)(&DAT_007d7c44 + param_2 * 0x1c8) = local_8[4];
        if ((char)local_8[5] == '\x01') {
          FUN__text__004c1f40(param_2,(uint)local_8[2] >> 0x1c,local_8[2] & 0xfffffff,0xfffffffe);
        }
      }
LAB__text__004c943f:
      local_8 = (int *)0x4c944f;
      FUN__text__0056ce80();
      return;
    }
    local_130 = FUN__text__004c1eb0(param_2,*local_11c >> 0x1c,*local_11c & 0xfffffff);
    local_134 = FUN__text__004c1eb0(param_2,local_11c[1] >> 0x1c,local_11c[1] & 0xfffffff);
    local_138 = FUN__text__004c1eb0(param_2,local_11c[2] >> 0x1c,local_11c[2] & 0xfffffff);
    local_13c = FUN__text__004c1eb0(param_2,local_11c[3] >> 0x1c,local_11c[3] & 0xfffffff);
    local_140 = local_11c[4];
    FUN__text__004d5ec0(local_12c,CONCAT22(extraout_var,local_130),
                        CONCAT22((short)(local_140 >> 0x10),local_134),local_138,
                        CONCAT22(extraout_var,local_13c));
    if (((local_120 & 0xffff) != 0) && (local_144 = local_144 + 1, (local_128 & 1) != 0)) {
      if ((char)local_8[5] == '\x01') {
        FUN__text__004c1f40(param_2,(uint)local_8[2] >> 0x1c,local_8[2] & 0xfffffff,
                            local_114 & 0xffff);
      }
      *(undefined2 *)(&DAT_007d7c4c + param_2 * 0x1c8) = 0;
      *(uint *)(&DAT_007d7c44 + param_2 * 0x1c8) = local_140;
      goto LAB__text__004c943f;
    }
    if ((local_10 & 0xffff) == 0) {
      FUN__text__0056d810(local_244,"MOUSE  %3d , %3d ,%3d ,%3d : HIT %4d",(int)local_130,
                          (int)local_134,(int)local_138,(int)local_13c,local_120 & 0xffff);
      FUN__text__00416370(0x1c2,((local_114 & 0xffff) + 3) * 0x10,0,local_244,0xff20ffa0);
      FUN__text__00410310((int)local_130,(int)local_134,(int)local_138,(int)local_13c,0,0x80ffff14,1
                         );
    }
    local_11c = local_11c + 5;
    local_114 = CONCAT22(local_114._2_2_,(short)local_114 + 1);
  } while( true );
}

