
void FUN__text__004b6690(short param_1,undefined2 param_2,undefined1 param_3,undefined1 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = &DAT_007e17e8 + param_1 * 0x4a0;
  FUN__text__004b66f0(local_c,CONCAT22((short)((uint)local_c >> 0x10),param_2),param_3,param_4);
  local_8 = 0x4b66e5;
  FUN__text__0056ce80();
  return;
}

