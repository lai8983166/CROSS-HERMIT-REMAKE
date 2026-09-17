
void FUN__text1__0080fb61(int param_1,int param_2,undefined4 param_3)

{
  byte bVar1;
  byte local_2444 [9264];
  undefined4 uStack_14;
  byte *pbStack_10;
  byte *pbStack_c;
  byte *local_8;
  
  local_8 = (byte *)0x80fb6e;
  FUN__text1__00848c20();
  local_8 = local_2444;
  pbStack_c = (byte *)0x80fb8c;
  FUN__text1__0080fc08();
  while (local_8 < (byte *)(param_1 + param_2)) {
    bVar1 = *local_8;
    local_8 = (byte *)param_3;
    pbStack_c = (byte *)(uint)bVar1;
    pbStack_10 = local_2444;
    uStack_14 = 0x80fbcb;
    FUN__text1__0080fcfd();
    local_8 = (byte *)(uint)bVar1;
    pbStack_c = local_2444;
    pbStack_10 = (byte *)0x80fbe7;
    FUN__text1__0080fdb3();
  }
  local_8 = (byte *)param_3;
  pbStack_c = (byte *)0x100;
  pbStack_10 = local_2444;
  uStack_14 = 0x80fc01;
  FUN__text1__0080fcfd();
  return;
}

