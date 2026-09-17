
void FUN__text__004bbcc0(void)

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
  FUN__text__004bd210();
  FUN__text__004bca40();
  FUN__text__004bbd40();
  *(undefined2 *)(local_8 + 0x32) = 0;
  if ((DAT_007a528e == 0xf) && (DAT_007a5290 == 4)) {
    *(undefined2 *)(local_8 + 0x32) = 1;
  }
  local_8 = 0x4bbd3c;
  FUN__text__0056ce80();
  return;
}

