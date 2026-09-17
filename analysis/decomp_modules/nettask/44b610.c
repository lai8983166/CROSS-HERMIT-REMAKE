
void FUN__text__0044b610(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = FUN__text__0041ae70();
  local_10 = 0;
  do {
    if (local_10 == 4) {
      local_8 = 0x44b72b;
      FUN__text__0056ce80();
      return;
    }
    if (*(char *)(local_c + local_10 * 0x88) == '\0') {
      FUN__text__00407780();
    }
    else {
      local_18 = local_c + 2 + local_10 * 0x88;
      FUN__text__004077c0(DAT_007a49fc);
      uVar6 = 1;
      uVar5 = *(undefined4 *)(local_8 + 0x1ba0);
      iVar3 = local_18;
      uVar2 = FUN__text__004142b0(uVar5,local_18,1);
      local_14 = FUN__text__00408e30(uVar2,uVar5,iVar3,uVar6);
      if ((local_14 != 0) &&
         (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_0060676c + 0xc,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_10 = local_10 + 1;
  } while( true );
}

