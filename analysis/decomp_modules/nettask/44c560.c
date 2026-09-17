
void __thiscall
FUN__text__0044c560(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
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
  local_c = param_1 + 0x1b8;
  local_8 = param_1;
  local_18 = FUN__text__0044c390(param_2,param_3);
  local_10 = 0;
  while( true ) {
    if (local_10 == 0x14) goto LAB__text__0044c667;
    FUN__text__004077c0(DAT_007a49fc);
    uVar7 = 0;
    uVar6 = *(undefined4 *)(local_18 + local_10 * 4);
    uVar5 = param_4;
    uVar2 = FUN__text__004142b0(param_4,uVar6,0);
    local_14 = FUN__text__00408e30(uVar2,uVar5,uVar6,uVar7);
    if ((local_14 != 0) &&
       (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606794 + 0xb,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (local_14 != 0) break;
    local_10 = local_10 + 1;
  }
  for (local_10 = 0; local_10 != 0x14; local_10 = local_10 + 1) {
    FUN__text__00407780();
  }
LAB__text__0044c667:
  local_8 = 0x44c674;
  FUN__text__0056ce80();
  return;
}

