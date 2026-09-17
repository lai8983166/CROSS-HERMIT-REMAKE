
int FUN__text__004d46e0(short param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 < 0) {
    iVar1 = (uint)(ushort)(param_1 >> 0xf) << 0x10;
  }
  else {
    iVar1 = CONCAT22(param_1 >> 0xf,(short)(char)(&DAT_007a5120)[param_1]);
  }
  return iVar1;
}

