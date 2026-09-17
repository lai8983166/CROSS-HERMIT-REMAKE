
void FUN__text__00459b10(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0xff00;
  do {
    FUN__text__00459cc0();
    local_10 = CONCAT31(local_10._1_3_,(char)((uint)local_c >> 8));
    FUN__text__00410310(0,0,0x403,0x300,0x50,local_10 << 0x18,1);
    FUN__text__00422360(0);
    local_c = local_c + -0x280;
    if (local_c < 0xff) break;
  } while ((*(uint *)(DAT_007a49fc + 0x1990) & 1) == 0);
  local_c = 10;
  do {
    FUN__text__00459cc0();
    FUN__text__00422360(0);
    local_c = local_c + -1;
  } while (local_c != 0);
  local_c = 0;
  do {
    FUN__text__00459cc0();
    FUN__text__00422360(0);
  } while (*(int *)(DAT_007a49fc + 0x19b8) != 3);
  local_c = 0;
  do {
    FUN__text__00459cc0();
    local_10 = CONCAT31(local_10._1_3_,(char)((uint)local_c >> 8));
    FUN__text__00410310(0,0,0x403,0x300,0x50,local_10 << 0x18,1);
    FUN__text__00422360(0);
    local_c = local_c + 0x800;
  } while (local_c < 0xff01);
  *(undefined4 *)(local_8 + 0x30) = 1;
  local_8 = 0x459cb5;
  FUN__text__0056ce80();
  return;
}

