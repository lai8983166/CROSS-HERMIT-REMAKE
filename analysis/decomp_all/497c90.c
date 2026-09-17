
void FUN__text__00497c90(void)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  sVar1 = (short)((uint)*(undefined4 *)(DAT_007a49f8 + 0x2490) >> 8);
  local_8 = CONCAT22(local_8._2_2_,sVar1);
  if (sVar1 != 0) {
    FUN__text__00410310(0,0,0x400,0x300,0x65,local_8 << 0x18,1);
  }
  local_8 = 0x497d0a;
  FUN__text__0056ce80();
  return;
}

