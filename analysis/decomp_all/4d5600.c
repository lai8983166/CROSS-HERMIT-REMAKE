
void FUN__text__004d5600(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  int local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  local_14 = 1;
  while (local_10 = local_10 + *(int *)(&DAT_006e4308 + local_14 * 4), local_10 <= param_1) {
    local_14 = local_14 + 1;
  }
  local_c = local_14 + -1;
  local_c = FUN__text__004d1ba0((int)local_c,1,0x87);
  local_8 = 0x4d5691;
  FUN__text__0056ce80();
  return;
}

