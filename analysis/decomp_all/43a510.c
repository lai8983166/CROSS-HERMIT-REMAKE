
void FUN__text__0043a510(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int *local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__004500b0("data\\Tactics\\mapcom.bin");
  iVar3 = FUN__text__0042ae20(uVar2);
  *local_8 = iVar3;
  if ((*local_8 == 0) &&
     (iVar3 = FUN__text__00424f80("MapCom!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9d0 + 5,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*local_8 != 0) {
    local_c = *local_8;
    iVar3 = FUN__text__004214f0(local_c,0);
    local_8[1] = iVar3;
    iVar3 = FUN__text__004214f0(local_c,1);
    local_8[0x23] = iVar3;
    iVar3 = FUN__text__004214f0(local_c,2);
    local_8[0x24] = iVar3;
    iVar3 = FUN__text__004214f0(local_c,3);
    local_8[0x25] = iVar3;
    local_c = local_8[1];
    for (local_10 = 0; local_10 != 0x21; local_10 = local_10 + 1) {
      iVar3 = FUN__text__004214f0(local_c,local_10);
      local_8[local_10 + 2] = iVar3;
    }
  }
  local_8 = (int *)0x43a636;
  FUN__text__0056ce80();
  return;
}

