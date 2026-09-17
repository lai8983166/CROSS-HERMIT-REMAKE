
/* WARNING: Removing unreachable block (ram,0x0045e704) */
/* WARNING: Removing unreachable block (ram,0x0045e711) */
/* WARNING: Removing unreachable block (ram,0x0045e7a4) */
/* WARNING: Removing unreachable block (ram,0x0045e7e4) */
/* WARNING: Removing unreachable block (ram,0x0045e8b3) */

void FUN__text__0045e5d0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [23];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00425ed0(0);
  FUN__text__00425ed0(1);
  (*API_GDI32_DLL_CreateFontA)(0x14,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  local_10 = FUN__text__0056ce80();
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00409480(local_10);
  }
  do {
    FUN__text__004263b0(DAT_007a49fc);
    FUN__text__00426820(DAT_007a49fc,0xa0,0xa0,0x14,0,local_8 + 0x1930,local_8 + 0x19bc,10);
    FUN__text__00422360(0);
  } while( true );
}

