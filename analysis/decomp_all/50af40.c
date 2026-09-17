
void FUN__text__0050af40(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0042ae20("data\\op\\opdata.bin");
  if (local_c != 0) {
    FUN__text__00416790(local_c,10);
    local_10 = local_c;
    FUN__text__00428ad0(local_c);
  }
  uVar4 = 0xb;
  uVar1 = FUN__text__004500b0("data\\OP\\OpData2.bin");
  FUN__text__00505e20(local_8 + 0x260,uVar1,uVar4);
  local_8 = 0x50afc7;
  FUN__text__0056ce80();
  return;
}

