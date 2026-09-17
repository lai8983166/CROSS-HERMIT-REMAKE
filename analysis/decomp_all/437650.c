
int FUN__text__00437650(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return (uint)DAT_007a2944 * 0x1000000 + (uint)DAT_007a2945 * 0x10000 + (uint)DAT_007a2946 * 0x100
         + (uint)DAT_007a2947;
}

