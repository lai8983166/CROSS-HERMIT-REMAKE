
void FUN__text__00450c70(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_14c [16];
  undefined1 local_10c [260];
  undefined4 local_8;
  
  puVar2 = local_14c;
  for (iVar1 = 0x52; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00450a60(param_1);
  if (iVar1 != 0) {
    FUN__text__0056d810(local_10c,&DAT_00592b28,param_1,"check.bin");
    iVar1 = FUN__text__0042a8e0(local_10c);
    if (iVar1 != 0) {
      FUN__text__0056d810(local_10c,&DAT_00592b28,param_1,"data.z");
      FUN__text__0042a8e0(local_10c);
    }
  }
  local_8 = 0x450d24;
  FUN__text__0056ce80();
  return;
}

