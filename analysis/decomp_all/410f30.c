
void __fastcall FUN__text__00410f30(undefined4 param_1)

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
  local_8 = param_1;
  local_c = FUN__text__00525b7e(PTR_IMAGE_DOS_HEADER_007a2728,0x800,&DAT_005cc1bc,param_1,0);
  uStack_1c = 0x410f88;
  FUN__text__0056ce80();
  return;
}

