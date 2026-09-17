
undefined4 FUN__text__004c4d80(uint param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return CONCAT22((short)((uint)(&DAT_00624520 + (param_1 & 0xffff) * 0x26) >> 0x10),
                  *(undefined2 *)(&DAT_00624520 + (param_1 & 0xffff) * 0x26));
}

