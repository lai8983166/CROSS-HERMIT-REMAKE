
void FUN__text__0044d730(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0044d610();
  FUN__text__004db060(3,1);
  FUN__text__00415420();
  FUN__text__00422360(0);
  _memset((void *)(local_8 + 0x30),0,8);
  local_c = 1;
  while (local_c != 0) {
    iVar1 = FUN__text__0044d810();
    if (iVar1 != 0) {
      local_c = 0;
    }
    FUN__text__0044d970();
    FUN__text__00422360(0);
  }
  FUN__text__004db230(0x5a);
  while( true ) {
    iVar1 = FUN__text__004db270();
    if (iVar1 != 0) break;
    FUN__text__00422360(0);
  }
  FUN__text__004db300();
  FUN__text__00439e30(1);
  local_8 = 0x44d800;
  FUN__text__0056ce80();
  return;
}

