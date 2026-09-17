
void FUN__text__00483cf0(int param_1,undefined4 param_2,undefined4 *param_3)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_bc [16];
  int local_7c;
  undefined *local_78;
  int local_74;
  undefined1 local_70 [44];
  short local_44;
  short sStack_42;
  short local_1c;
  undefined4 local_18;
  undefined2 local_14;
  undefined1 uStack_12;
  undefined1 uStack_11;
  undefined2 local_10;
  short sStack_e;
  short *local_c;
  undefined4 local_8;
  
  puVar3 = local_bc;
  for (iVar2 = 0x2e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_78 = &DAT_006c30e0;
  FUN__text__004deaa0(param_1,&local_44);
  FUN__text__004deaa0(param_2,local_70);
  FUN__text__0046b3e0(param_1,&local_44);
  FUN__text__0046b3e0(param_2,local_70);
  local_44 = local_44 + *(short *)(local_78 + 0x20) +
             (short)((int)((uint)*(byte *)(*(int *)(param_1 + 600) + 5) *
                          (int)*(short *)(local_78 + 0x22)) / 100);
  sStack_42 = sStack_42 + *(short *)(local_78 + 0x24) +
              (short)((int)((uint)*(byte *)(*(int *)(param_1 + 600) + 5) *
                           (int)*(short *)(local_78 + 0x26)) / 100);
  local_74 = FUN__text__004824d0(&local_44,local_70);
  if ((local_74 != 0) && (iVar2 = FUN__text__004692e0(param_2), iVar2 != 0)) {
    local_74 = 1;
  }
  local_18 = *param_3;
  uStack_11 = (undefined1)((uint)param_3[1] >> 0x18);
  _local_14 = CONCAT12((undefined1)local_74,(short)param_3[1]);
  _local_10 = CONCAT22(-local_1c,(short)param_3[2]);
  local_7c = local_74;
  switch(local_74) {
  case 0:
    FUN__text__004950c0(param_1);
    break;
  case 1:
  case 2:
  case 3:
    FUN__text__0046beb0(param_2,0xbc3,0,0,0,&local_18);
    break;
  case 4:
    local_c = (short *)(&DAT_00613b78 + *(short *)(param_3 + 1) * 6);
    puVar3 = &local_18;
    uVar6 = 0;
    uVar5 = 0;
    uVar4 = 0;
    sVar1 = *local_c;
    iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f18 + 0x33);
    FUN__text__0046beb0(param_2,(int)sVar1 + iVar2 % 5,uVar4,uVar5,uVar6,puVar3);
  }
  local_8 = 0x483ec9;
  FUN__text__0056ce80();
  return;
}

