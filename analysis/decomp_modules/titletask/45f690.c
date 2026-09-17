
void FUN__text__0045f690(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0xff00;
  do {
    FUN__text__0045f9c0(param_1);
    FUN__text__0045fe70();
    local_10 = CONCAT31(local_10._1_3_,(char)((uint)local_c >> 8));
    FUN__text__00410310(0,0,0x403,0x300,0x50,local_10 << 0x18,1);
    FUN__text__00422360(0);
    local_c = local_c + -0x800;
  } while (0 < local_c);
  local_8 = 0x45f73d;
  FUN__text__0056ce80();
  return;
}

