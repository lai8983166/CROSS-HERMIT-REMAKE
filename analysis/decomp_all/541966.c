
uint FUN__text__00541966(int *param_1,undefined4 param_2,uint param_3)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  
  if (param_1[4] != 0xce) {
    *(undefined4 *)(*param_1 + 0x14) = 0x12;
    *(int *)(*param_1 + 0x18) = param_1[4];
    (**(code **)*param_1)(param_1);
  }
  if ((uint)param_1[0x18] <= (uint)param_1[0x1e]) {
    *(undefined4 *)(*param_1 + 0x14) = 0x77;
    (**(code **)(*param_1 + 4))(param_1,0xffffffff);
    return 0;
  }
  if (param_1[2] != 0) {
    *(int *)(param_1[2] + 4) = param_1[0x1e];
    *(int *)(param_1[2] + 8) = param_1[0x18];
    (**(code **)param_1[2])(param_1);
  }
  uVar3 = param_1[0x45] * param_1[0x44];
  if (param_3 < uVar3) {
    *(undefined4 *)(*param_1 + 0x14) = 0x15;
    (**(code **)*param_1)(param_1);
  }
  iVar1 = (**(code **)(param_1[0x61] + 0xc))(param_1,param_2);
  uVar2 = 0;
  if (iVar1 != 0) {
    param_1[0x1e] = param_1[0x1e] + uVar3;
    uVar2 = uVar3;
  }
  return uVar2;
}

