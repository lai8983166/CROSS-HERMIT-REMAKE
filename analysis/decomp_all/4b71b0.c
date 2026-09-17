
void FUN__text__004b71b0(uint param_1,undefined4 param_2,undefined1 param_3,undefined2 param_4,
                        undefined2 param_5,undefined2 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined2 *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = (param_1 & 0xffff) * 10;
  local_c = (undefined2 *)(&DAT_0061c120 + iVar1);
  FUN__text__004b7230(CONCAT22((short)((uint)local_c >> 0x10),param_4),param_5,0,0,
                      (&DAT_0061c128)[iVar1],param_6,*local_c,param_2,param_3);
  local_8 = 0x4b7220;
  FUN__text__0056ce80();
  return;
}

