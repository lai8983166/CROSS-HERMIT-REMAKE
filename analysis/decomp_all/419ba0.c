
void FUN__text__00419ba0(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_2e0 [16];
  undefined4 local_2a0 [2];
  int local_298;
  undefined1 local_294 [256];
  undefined1 local_194 [388];
  undefined4 uStack_10;
  
  puVar3 = local_2e0;
  for (iVar2 = 0xb7; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0056cd86(0x101,local_194);
  if (iVar2 == 0) {
    FUN__text__0056cd80(local_294,0x100);
    local_298 = FUN__text__0056cd7a(local_294);
    if (local_298 == 0) {
      FUN__text__0056cd6e();
    }
    else {
      FUN__text__0056d4d0(local_2a0,**(undefined4 **)(local_298 + 0xc),4);
      uVar1 = FUN__text__0056cd74(local_2a0[0]);
      FUN__text__0056cd90(param_1,uVar1);
    }
  }
  uStack_10 = 0x419c53;
  FUN__text__0056ce80();
  return;
}

