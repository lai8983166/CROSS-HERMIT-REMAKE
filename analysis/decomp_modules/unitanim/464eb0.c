
void __thiscall
FUN__text__00464eb0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5)

{
  code *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_50;
  for (iVar4 = 0x13; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if (*(short *)(param_1 + 0x48) != -1) {
    if (*(int *)(param_1 + 0x44) == 0) {
      local_10 = 0;
    }
    else {
      local_10 = *(int *)(param_1 + 0x44) + 0x844;
    }
    local_8 = param_1;
    uVar2 = FUN__text__004500b0(param_2);
    iVar4 = local_10;
    uVar3 = FUN__text__004142b0(local_10,uVar2,param_3,param_4,param_5);
    local_c = FUN__text__00409b70(uVar3,iVar4,uVar2,param_3,param_4,param_5);
    if ((local_c != 0) &&
       (iVar4 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitAnim.cpp",
                                    DAT_00610524 + 6,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x464f75;
  FUN__text__0056ce80();
  return;
}

