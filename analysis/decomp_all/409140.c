
void __thiscall FUN__text__00409140(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x4c) != 0) {
    uVar6 = 1;
    uVar5 = 0;
    uVar4 = 0;
    local_8 = param_1;
    uVar1 = FUN__text__004142b0(param_2,0,0,1);
    FUN__text__00404b90(uVar1,param_2,uVar4,uVar5,uVar6);
  }
  local_8 = 0x409198;
  FUN__text__0056ce80();
  return;
}

