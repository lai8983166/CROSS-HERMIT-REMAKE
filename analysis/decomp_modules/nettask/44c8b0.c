
void __fastcall FUN__text__0044c8b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_90 [16];
  int local_50;
  undefined1 local_4c [64];
  int local_c;
  int local_8;
  
  puVar2 = local_90;
  for (iVar1 = 0x23; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x1a54;
  local_8 = param_1;
  FUN__text__0056d810(local_4c,&DAT_00598580,param_1 + 0x1a60);
  local_50 = FUN__text__00418f70(local_4c,4,*(undefined4 *)(local_8 + 0x34));
  if (local_50 == 0) {
    *(undefined4 *)(local_c + 0x30) = 0;
    FUN__text__00419950(local_c + 0xc);
  }
  local_8 = 0x44c963;
  FUN__text__0056ce80();
  return;
}

