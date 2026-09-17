
void FUN__text__00457500(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_8c [16];
  int local_4c;
  undefined1 local_48 [64];
  int local_8;
  
  puVar2 = local_8c;
  for (iVar1 = 0x22; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if (iVar1 != 0) {
    FUN__text__00457730(0x60,0x10,1,local_8 + 0x117dd8,"0:Total");
    FUN__text__00457730(0x60,0x20,1,local_8 + 0x117df8,"1:SEND");
    FUN__text__00457730(0x60,0x30,1,local_8 + 0x117e18,"2:Ewait");
    FUN__text__00457730(0x100,0x30,1,local_8 + 0x117e38,&DAT_005953ac);
    FUN__text__00457730(0x60,0x40,1,local_8 + 0x117e58,"4:Ssb");
    FUN__text__00457730(0x60,0x50,1,local_8 + 0x117e78,"5:Rcl");
    FUN__text__00457730(0x100,0x50,1,local_8 + 0x117e98,&DAT_005953ac);
    FUN__text__0056d810(local_48,"com:%04d(%08x) : %d",*(undefined4 *)(local_8 + 0x117f18),
                        *(undefined4 *)(local_8 + 0x117f1c),*(undefined4 *)(local_8 + 0x188));
    FUN__text__0040ec50(0x60,0x70,1,0xffff0000,0,local_48);
    FUN__text__0056d810(local_48,"NET:CNT%08x\n",*(undefined4 *)(local_8 + 0x178));
    FUN__text__0040ec50(0,0x80,1,0xffff0000,0,local_48);
    for (local_4c = 0; local_4c != 4; local_4c = local_4c + 1) {
      FUN__text__0056d810(local_48,"%10d:%8x:%10d\n",
                          *(undefined4 *)(local_8 + 0x117d98 + local_4c * 4),
                          *(undefined4 *)(local_8 + 0x117da8 + local_4c * 4),
                          *(undefined4 *)(local_8 + 0x117db8 + local_4c * 4));
      FUN__text__0040ec50(0,(local_4c + 9) * 0x10,1,0xffffffff,0,local_48);
    }
  }
  local_8 = 0x45771f;
  FUN__text__0056ce80();
  return;
}

