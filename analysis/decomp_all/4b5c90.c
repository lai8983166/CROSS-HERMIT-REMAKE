
undefined4 __thiscall FUN__text__004b5c90(undefined4 param_1,int param_2,uint param_3)

{
  byte bVar1;
  bool bVar2;
  ushort uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_c0 [18];
  uint local_78;
  ushort local_70 [14];
  ushort local_54;
  undefined2 uStack_52;
  short local_50;
  ushort local_4c;
  short asStack_4a [21];
  undefined *local_20;
  undefined *local_1c;
  undefined *local_18;
  int local_14;
  ushort local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined4 local_8;
  
  puVar5 = local_c0;
  for (iVar4 = 0x2f; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_8 = param_1;
  _local_10 = CONCAT22(uStack_e,*(ushort *)(param_2 + 6));
  local_14 = param_2 + 0xb0 + ((param_3 & 0xffff) - 1) * 0xc;
  local_18 = &DAT_006c2dc8 + (param_3 & 0xffff) * 0x48;
  local_1c = &DAT_006e4158;
  local_20 = &DAT_006e4158 + (uint)*(ushort *)(param_2 + 6) * 0xd;
  bVar1 = (&DAT_006b2d8a)[*(short *)(param_2 + 6) * 0x40];
  _local_54 = CONCAT22(uStack_52,(ushort)bVar1);
  local_70[0] = 0;
  local_70[1] = 1;
  local_70[2] = 2;
  local_70[3] = 3;
  local_70[4] = 3;
  local_70[5] = 4;
  local_70[6] = 4;
  local_70[7] = 5;
  local_70[8] = 5;
  local_70[9] = 5;
  local_70[10] = 5;
  local_70[0xb] = 5;
  local_70[0xc] = 0;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 0x14) {
    asStack_4a[(local_c & 0xffff) + 1] = 0;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < (uint)(byte)(&DAT_006b2d8b)[*(short *)(param_2 + 6) * 0x40]) {
    if (*(short *)(param_2 + 0x52 + (local_c & 0xffff) * 2) != 0) {
      uVar3 = (ushort)(byte)(&DAT_006c2dcc)
                            [*(short *)(param_2 + 0x52 + (local_c & 0xffff) * 2) * 0x48];
      _local_4c = CONCAT22(asStack_4a[0],uVar3);
      asStack_4a[uVar3] = asStack_4a[uVar3] + 1;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  uVar3 = (byte)(&DAT_006c2dcc)[(param_3 & 0xffff) * 0x48] - 1;
  _local_4c = CONCAT22(asStack_4a[0],uVar3);
  local_50 = (byte)local_1c[uVar3 + 1] - 1;
  bVar2 = true;
  if (local_20[uVar3 + 1] == '\0') {
    bVar2 = false;
  }
  else if ((byte)local_20[uVar3 + 1] < (byte)local_18[7]) {
    bVar2 = false;
  }
  else if ((local_50 < 0) || (asStack_4a[local_50 + 1] == 0)) {
    if ((local_18[6] == '\x02') &&
       (local_78 = (uint)(byte)local_18[4], (ushort)bVar1 != local_70[local_78])) {
      bVar2 = false;
    }
  }
  else {
    bVar2 = false;
  }
  switch(*(undefined1 *)(local_14 + 8)) {
  case 2:
    if (!bVar2) {
      *(undefined1 *)(local_14 + 8) = 4;
    }
    break;
  case 3:
    if (!bVar2) {
      *(undefined1 *)(local_14 + 8) = 5;
    }
    break;
  case 4:
    if (bVar2) {
      *(undefined1 *)(local_14 + 8) = 2;
    }
    break;
  case 5:
    if (bVar2) {
      *(undefined1 *)(local_14 + 8) = 3;
    }
  }
  return 1;
}

