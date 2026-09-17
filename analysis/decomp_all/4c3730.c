
void FUN__text__004c3730(undefined4 param_1,undefined4 param_2)

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
  local_c = param_2;
  local_10 = local_10 & 0xffff0000;
  while ((local_10 & 0xffff) < 0x14) {
    FUN__text__004cb820();
    local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
  }
  local_8 = 0x4c37a7;
  FUN__text__0056ce80();
  return;
}

