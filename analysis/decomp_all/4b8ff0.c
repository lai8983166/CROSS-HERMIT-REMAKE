
void FUN__text__004b8ff0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  uint local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (DAT_007a5296 == DAT_007a5298) {
    FUN__text__00439e30(0xc);
  }
  else {
    local_10 = CONCAT22(local_10._2_2_,DAT_007a5296);
    FUN__text__004da860((int)*(short *)(&DAT_007a5308 + (uint)DAT_007a5296 * 0x70));
    FUN__text__004b9210();
    local_c = (uint)local_c._2_2_ << 0x10;
    while ((int)(local_c & 0xffff) < (int)*(short *)(&DAT_007a52f8 + (local_10 & 0xffff) * 0x70)) {
      FUN__text__004b9270(CONCAT22(*(short *)(&DAT_007a52f8 + (local_10 & 0xffff) * 0x70) >> 0xf,
                                   *(undefined2 *)
                                    (&DAT_007a52d0 +
                                    (local_c & 0xffff) * 2 + (local_10 & 0xffff) * 0x70)));
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    FUN__text__004b92c0();
    DAT_007a5296 = DAT_007a5296 + 1;
    FUN__text__00439e30(0x10);
  }
  FUN__text__00422360(0);
  local_8 = 0x4b910b;
  FUN__text__0056ce80();
  return;
}

