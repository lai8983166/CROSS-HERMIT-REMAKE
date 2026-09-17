
void __thiscall FUN__text__004cb220(int param_1,undefined2 param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  uint local_24;
  undefined4 local_20;
  uint local_1c;
  uint local_18;
  undefined2 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0x37;
  local_10 = 1;
  local_14 = 0xff;
  local_1c = CONCAT22(local_1c._2_2_,*(undefined2 *)(param_1 + 0x16));
  local_20 = local_20 & 0xffff0000;
  local_18 = local_18 & 0xffff0000;
  local_8 = param_1;
  while ((local_18 & 0xffff) < (local_1c & 0xffff)) {
    local_24 = (uint)*(ushort *)(local_8 + 0x18 + (local_18 & 0xffff) * 0x110);
    switch(local_24) {
    case 0:
      local_20 = (uint)local_20._2_2_ << 0x10;
      break;
    case 1:
      local_20 = CONCAT22(local_20._2_2_,1);
      local_10 = 1;
      local_14 = 0xff;
      break;
    case 2:
      local_20 = (uint)local_20._2_2_ << 0x10;
      if ((local_18 & 0xffff) == 0) {
        *(undefined2 *)(local_8 + 0x18 + (local_18 & 0xffff) * 0x110) = 3;
      }
      else if (*(short *)(local_8 + 0x22 + ((local_18 & 0xffff) - 1) * 0x110) != 0) {
        *(undefined2 *)(local_8 + 0x18 + (local_18 & 0xffff) * 0x110) = 3;
      }
      break;
    case 3:
      *(short *)(local_8 + 0x1a + (local_18 & 0xffff) * 0x110) =
           *(short *)(local_8 + 0x1a + (local_18 & 0xffff) * 0x110) + 1;
      if (*(short *)(local_8 + 0x1c + (local_18 & 0xffff) * 0x110) <
          *(short *)(local_8 + 0x1a + (local_18 & 0xffff) * 0x110)) {
        *(undefined2 *)(local_8 + 0x18 + (local_18 & 0xffff) * 0x110) = 1;
        *(undefined2 *)(local_8 + 0x1a + (local_18 & 0xffff) * 0x110) =
             *(undefined2 *)(local_8 + 0x1c + (local_18 & 0xffff) * 0x110);
      }
      local_20 = CONCAT22(local_20._2_2_,1);
      local_10 = 1;
      local_14 = (undefined2)
                 ((*(short *)(local_8 + 0x1a + (local_18 & 0xffff) * 0x110) * 0xff) /
                 (int)*(short *)(local_8 + 0x1c + (local_18 & 0xffff) * 0x110));
    }
    if ((local_20 & 0xffff) != 0) {
      FUN__text__004cbf00(local_8 + 0x28 + (local_18 & 0xffff) * 0x110,param_2,param_3,local_10,
                          local_14,0xff,0xff,0xff,local_c);
      param_3 = param_3 + *(short *)(local_8 + 0x6a + (local_18 & 0xffff) * 0x110);
    }
    if ((((local_18 & 0xffff) == 0) ||
        (*(short *)(local_8 + 0x22 + ((local_18 & 0xffff) - 1) * 0x110) == 1)) &&
       (*(short *)(local_8 + 0x1e + (local_18 & 0xffff) * 0x110) =
             *(short *)(local_8 + 0x1e + (local_18 & 0xffff) * 0x110) + 1,
       *(short *)(local_8 + 0x20 + (local_18 & 0xffff) * 0x110) <
       *(short *)(local_8 + 0x1e + (local_18 & 0xffff) * 0x110))) {
      *(undefined2 *)(local_8 + 0x1e + (local_18 & 0xffff) * 0x110) =
           *(undefined2 *)(local_8 + 0x20 + (local_18 & 0xffff) * 0x110);
      *(undefined2 *)(local_8 + 0x22 + (local_18 & 0xffff) * 0x110) = 1;
    }
    local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
  }
  local_8 = 0x4cb5d4;
  FUN__text__0056ce80();
  return;
}

