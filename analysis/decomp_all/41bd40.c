
void FUN__text__0041bd40(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [13];
  undefined4 uStack_1c;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00422360(0);
  FUN__text__0042b240(1);
  (*DAT_00592354)(PTR_IMAGE_DOS_HEADER_007a2728,0x98,0,FUN__text__0041be10,local_8);
  local_c = FUN__text__0056ce80();
  FUN__text__0042b240(0);
  local_10 = local_c;
  if ((local_c < 0) || (1 < local_c)) {
    FUN__text__00419240();
  }
  else if ((*(char *)(local_8 + 6000) == '\0') &&
          (iVar2 = FUN__text__00424f80("SessionJoin!=0",
                                       "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                       DAT_005ff598 + 0x15,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  uStack_1c = 0x41be04;
  FUN__text__0056ce80();
  return;
}

