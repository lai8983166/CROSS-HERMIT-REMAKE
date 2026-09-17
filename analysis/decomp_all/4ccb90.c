
void __thiscall FUN__text__004ccb90(int param_1,int param_2)

{
  ushort uVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  uint local_18;
  uint local_14;
  undefined1 local_10 [4];
  uint local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = local_c >> 8;
  local_c = local_c & 0xffffff00;
  local_18 = (uint)*(ushort *)(param_1 + 0x26 + param_2 * 0x1c8);
  local_8 = param_1;
  if (local_18 == 0xc) {
    uVar1 = *(ushort *)(param_1 + 0x28 + param_2 * 0x1c8);
    *(short *)(param_1 + 0x28 + param_2 * 0x1c8) = *(short *)(param_1 + 0x28 + param_2 * 0x1c8) + 1;
    if ((int)(*(ushort *)(param_1 + 0x2a + param_2 * 0x1c8) - 1) < (int)(uint)uVar1) {
      local_c = CONCAT31((int3)uVar2,1);
    }
  }
  else if (local_18 == 0xd) {
    iVar3 = FUN__text__004128f0(0x39,0);
    if (iVar3 != 0) {
      local_c = CONCAT31(local_c._1_3_,1);
      if (DAT_007a49fc != 0) {
        FUN__text__0041e500();
      }
    }
    FUN__text__004ccb30(0,0,local_10,&local_14);
    if ((local_14 & 7) != 0) {
      local_c = CONCAT31(local_c._1_3_,1);
    }
    uVar1 = *(ushort *)(local_8 + 0x28 + param_2 * 0x1c8);
    *(short *)(local_8 + 0x28 + param_2 * 0x1c8) = *(short *)(local_8 + 0x28 + param_2 * 0x1c8) + 1;
    if ((int)(*(ushort *)(local_8 + 0x2a + param_2 * 0x1c8) - 1) < (int)(uint)uVar1) {
      local_c = CONCAT31(local_c._1_3_,1);
    }
  }
  else if (local_18 == 0xe) {
    iVar3 = FUN__text__004128f0(0x39,0);
    if (iVar3 != 0) {
      local_c = CONCAT31(local_c._1_3_,1);
      if (DAT_007a49fc != 0) {
        FUN__text__0041e500();
      }
    }
    FUN__text__004ccb30(0,0,local_10,&local_14);
    if ((local_14 & 7) != 0) {
      *(undefined4 *)(local_8 + 0x1c + param_2 * 0x1c8) =
           *(undefined4 *)(local_8 + 0x2c + param_2 * 0x1c8);
      local_c = CONCAT31(local_c._1_3_,1);
    }
    uVar1 = *(ushort *)(local_8 + 0x28 + param_2 * 0x1c8);
    *(short *)(local_8 + 0x28 + param_2 * 0x1c8) = *(short *)(local_8 + 0x28 + param_2 * 0x1c8) + 1;
    if ((int)(*(ushort *)(local_8 + 0x2a + param_2 * 0x1c8) - 1) < (int)(uint)uVar1) {
      local_c = CONCAT31(local_c._1_3_,1);
    }
  }
  if ((local_c & 0xff) == 1) {
    *(undefined1 *)(local_8 + 0x1cd) = 0;
  }
  local_8 = 0x4cce16;
  FUN__text__0056ce80();
  return;
}

