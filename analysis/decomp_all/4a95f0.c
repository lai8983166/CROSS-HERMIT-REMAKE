
void FUN__text__004a95f0(undefined4 *param_1,short param_2)

{
  undefined2 uVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_94 [16];
  char local_54;
  short local_50;
  short local_4c;
  short local_48;
  short local_44;
  short local_40;
  short local_3c;
  short local_38;
  short local_34;
  short local_30;
  short asStack_2c [10];
  undefined4 local_18;
  uint local_14;
  undefined4 local_10;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar4 = local_94;
  for (iVar3 = 0x24; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_18 = 0;
  local_14 = local_14 & 0xffff0000;
  local_30 = 0;
  local_3c = 0;
  local_40 = 0;
  local_44 = 0;
  *(undefined2 *)(&DAT_007aaaae + param_2 * 2) = 0xffff;
  *(undefined2 *)(&DAT_007aaae0 + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaae2 + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaae4 + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaae6 + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaaa4 + param_2 * 2) = 0xffff;
  *(undefined2 *)(&DAT_007aaab8 + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaaba + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaabc + param_2 * 8) = 0xffff;
  *(undefined2 *)(&DAT_007aaabe + param_2 * 8) = 0xffff;
  if (*(short *)(&DAT_007aaa12 + param_2 * 0x1c) == -1) {
    *param_1 = 0;
    param_1[1] = local_14;
    param_1[2] = local_10;
    *(undefined2 *)(param_1 + 3) = local_c;
  }
  else {
    asStack_2c[0] = *(short *)(&DAT_007aaa12 + param_2 * 0x1c);
    local_30 = 1;
    uVar1 = FUN__text__004d45c0(CONCAT22(*(short *)(&DAT_007aaa12 + param_2 * 0x1c) >> 0xf,
                                         *(undefined2 *)(&DAT_007aaa12 + param_2 * 0x1c)));
    *(undefined2 *)(&DAT_007aaaae + param_2 * 2) = uVar1;
    *(undefined2 *)(&DAT_007aaaa4 + param_2 * 2) = *(undefined2 *)(&DAT_007aaa12 + param_2 * 0x1c);
    local_44 = 0;
    for (local_34 = 0; local_34 < 4; local_34 = local_34 + 1) {
      if (*(short *)(&DAT_007aaa22 + local_34 * 2 + param_2 * 0x1c) != -1) {
        asStack_2c[local_30] = *(short *)(&DAT_007aaa22 + local_34 * 2 + param_2 * 0x1c);
        sVar2 = local_30 >> 0xf;
        local_44 = local_44 + 1;
        local_30 = local_30 + 1;
        uVar1 = FUN__text__004d45c0(CONCAT22(sVar2,*(undefined2 *)
                                                    (&DAT_007aaa22 + local_34 * 2 + param_2 * 0x1c))
                                   );
        *(undefined2 *)(&DAT_007aaae0 + param_2 * 8 + local_34 * 2) = uVar1;
        *(undefined2 *)(&DAT_007aaab8 + param_2 * 8 + local_34 * 2) =
             *(undefined2 *)(&DAT_007aaa22 + local_34 * 2 + param_2 * 0x1c);
      }
    }
    if (local_44 == 0) {
      local_18 = CONCAT22(local_18._2_2_,1);
      *param_1 = local_18;
      param_1[1] = local_14;
      param_1[2] = local_10;
      *(undefined2 *)(param_1 + 3) = local_c;
    }
    else {
      local_3c = 0;
      for (local_34 = 0; local_34 < local_30; local_34 = local_34 + 1) {
        for (local_38 = 0; local_38 < local_30; local_38 = local_38 + 1) {
          local_4c = asStack_2c[local_34];
          local_50 = asStack_2c[local_38];
          if (local_4c != local_50) {
            sVar2 = FUN__text__004d3a20((int)local_4c,CONCAT22(local_34 >> 0xf,local_50));
            local_3c = local_3c + sVar2;
            local_40 = local_40 + 1;
          }
        }
      }
      local_48 = local_3c / local_40;
      local_54 = (&DAT_007aaa15)[param_2 * 0x1c];
      if (local_54 == '\x01') {
        if (*(short *)(&DAT_007aaa1a + param_2 * 0x1c) < 0) {
          local_18 = CONCAT22(local_48,5);
        }
        else {
          local_18 = CONCAT22(local_48,4);
          local_14 = (uint)*(ushort *)(&DAT_007aaa18 + param_2 * 0x1c) << 0x10;
          local_10 = CONCAT22(*(undefined2 *)(&DAT_007aaa1c + param_2 * 0x1c),
                              *(undefined2 *)(&DAT_007aaa1a + param_2 * 0x1c));
          local_c = *(undefined2 *)(&DAT_007aaa1e + param_2 * 0x1c);
        }
      }
      else {
        if (DAT_007aab0a == 0) {
          local_18 = CONCAT22(local_48,3);
        }
        else {
          local_18 = CONCAT22(local_48,2);
          local_14 = (uint)DAT_007aab10 << 0x10;
          local_10 = CONCAT22(DAT_007aab16,DAT_007aab12);
          local_c = DAT_007aab14;
        }
      }
      if (local_18._2_2_ < 0x5b) {
        if (local_18._2_2_ < 0x4c) {
          if (local_18._2_2_ < 0x3d) {
            if (local_18._2_2_ < 0x2e) {
              if (local_18._2_2_ < 0x1f) {
                if (local_18._2_2_ < 0x10) {
                  local_14 = CONCAT22(local_14._2_2_,1);
                }
                else {
                  local_14 = CONCAT22(local_14._2_2_,2);
                }
              }
              else {
                local_14 = CONCAT22(local_14._2_2_,3);
              }
            }
            else {
              local_14 = CONCAT22(local_14._2_2_,4);
            }
          }
          else {
            local_14 = CONCAT22(local_14._2_2_,5);
          }
        }
        else {
          local_14 = CONCAT22(local_14._2_2_,6);
        }
      }
      else {
        local_14 = CONCAT22(local_14._2_2_,7);
      }
      *param_1 = local_18;
      param_1[1] = local_14;
      param_1[2] = local_10;
      *(undefined2 *)(param_1 + 3) = local_c;
    }
  }
  local_8 = 0x4a9aa4;
  FUN__text__0056ce80();
  return;
}

