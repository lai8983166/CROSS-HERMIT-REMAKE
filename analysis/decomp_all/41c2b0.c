
void FUN__text__0041c2b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [12];
  undefined4 uStack_1c;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0042b240(1);
  (*DAT_00592354)(PTR_IMAGE_DOS_HEADER_007a2728,0x99,0,FUN__text__0041c320,local_8);
  local_c = FUN__text__0056ce80();
  FUN__text__0042b240(0);
  uStack_1c = 0x41c31a;
  FUN__text__0056ce80();
  return;
}

