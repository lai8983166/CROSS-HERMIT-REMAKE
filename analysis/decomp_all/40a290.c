
void FUN__text__0040a290(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined2 param_4
                        ,undefined2 param_5,undefined2 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0040b890();
  iVar1 = DAT_00791730;
  if (DAT_00791730 != 0) {
    while (local_10 = iVar1 + -1, -1 < local_10) {
      local_c = *(undefined4 *)(&DAT_00791734 + local_10 * 4);
      FUN__text__0040b0f0(local_c,param_1,param_2,param_3,
                          CONCAT22((short)((uint)local_c >> 0x10),param_4),
                          CONCAT22((short)((uint)local_10 >> 0x10),param_5),param_6);
      iVar1 = local_10;
    }
  }
  local_8 = 0x40a31f;
  FUN__text__0056ce80();
  return;
}

