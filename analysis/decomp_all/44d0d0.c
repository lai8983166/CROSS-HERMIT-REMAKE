
void FUN__text__0044d0d0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_d0 [16];
  undefined1 local_90 [128];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_d0;
  for (iVar1 = 0x33; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0041ae70();
  for (local_10 = 0; local_10 != 0x10; local_10 = local_10 + 1) {
    FUN__text__0056d810(local_90,"(%02d) : %08x : RD(%d) : UD(%d) : %s\n",local_10,
                        *(undefined4 *)(local_c + 0x84 + local_10 * 0x88),
                        (int)*(char *)(local_c + 1 + local_10 * 0x88),
                        (int)*(char *)(local_c + local_10 * 0x88),local_c + 2 + local_10 * 0x88);
    FUN__text__0040ec50(0xa0,local_10 * 0x10 + 0x140,1,0xffffffff,0,local_90);
  }
  local_8 = 0x44d1c8;
  FUN__text__0056ce80();
  return;
}

