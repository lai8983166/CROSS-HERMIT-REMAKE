
void __fastcall FUN__text__004aa320(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  uint local_24;
  short local_20;
  uint local_1c [3];
  uint local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_20 = -1;
  local_24 = local_24 & 0xffff0000;
  local_8 = param_1;
  while ((local_24 & 0xffff) < 6) {
    FUN__text__004d5c40(local_1c,(local_24 & 0xffff) + 0x2c);
    local_c = &DAT_0061b208 + ((local_24 & 0xffff) + 5) * 0x10;
    if ((local_10 & 0xffff) != 0) {
      if ((local_1c[0] & 1) != 0) {
        local_20 = (short)local_24;
        FUN__text__004db2b0(5);
      }
      FUN__text__004d2ca0(*local_c,0x7c,*(undefined2 *)(local_c + 2),*(undefined2 *)(local_c + 0xc),
                          *(undefined2 *)(local_c + 0xe),*(undefined2 *)(local_c + 4),
                          *(undefined2 *)(local_c + 6),*(undefined2 *)(local_c + 8),
                          *(undefined2 *)(local_c + 10));
    }
    local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
  }
  local_20 = local_20 + 1;
  FUN__text__004d5ec0(local_1c,0x39e,0xc,0x5a,0x14);
  if ((local_10 & 0xffff) != 0) {
    FUN__text__004d68b0(&DAT_0061b5a8,0x70,0x39e,10,1);
    if ((local_1c[0] & 1) != 0) {
      FUN__text__004db2b0(5);
      local_20 = 7;
    }
  }
  local_8 = 0x4aa49d;
  FUN__text__0056ce80();
  return;
}

