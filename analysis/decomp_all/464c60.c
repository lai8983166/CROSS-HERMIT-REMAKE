
void FUN__text__00464c60(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00409900();
  *(undefined2 *)(local_8 + 0x48) = 0xffff;
  *(undefined4 *)(local_8 + 0x44) = 0;
  *(undefined4 *)(local_8 + 0x4c) = 0;
  *(undefined4 *)(local_8 + 0x50) = 0;
  local_8 = 0x464cbc;
  FUN__text__0056ce80();
  return;
}

