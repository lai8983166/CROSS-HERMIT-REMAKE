
undefined4 FUN__text__004ae2f0(uint param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = (param_1 & 0xffff) + (param_2 & 0xffff) * 0xc;
  return CONCAT22((short)((uint)iVar1 >> 0x10),*(undefined2 *)(&DAT_0061ba30 + iVar1 * 2));
}

