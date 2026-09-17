
void FUN__text__0044c490(undefined4 param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = FUN__text__0044c2c0(param_1);
  FUN__text__004077c0(DAT_007a49fc);
  uVar6 = 0;
  uVar5 = local_c;
  uVar2 = FUN__text__004142b0(param_2,local_c,0);
  local_10 = FUN__text__00408e30(uVar2,param_2,uVar5,uVar6);
  if ((local_10 != 0) &&
     (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606790 + 8,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_10 != 0) {
    FUN__text__00407780();
  }
  local_8 = 0x44c54c;
  FUN__text__0056ce80();
  return;
}

