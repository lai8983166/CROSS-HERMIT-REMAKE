
void __thiscall FUN__text__0040e510(int param_1,int param_2,undefined2 param_3)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(int *)(param_1 + 0x20) == 1) {
    local_c = *(int *)(param_2 + 4) + -1;
    uVar3 = (undefined2)((uint)*(int *)(param_2 + 4) >> 0x10);
    uVar2 = (undefined2)((uint)local_c >> 0x10);
    local_8 = param_1;
    switch(local_c) {
    case 0:
      FUN__text__0040e650(param_2,CONCAT22(uVar3,param_3));
      break;
    case 1:
      FUN__text__0040ea80(param_2,CONCAT22(uVar2,param_3));
      break;
    case 2:
      FUN__text__0040eb90(param_2,CONCAT22(uVar2,param_3));
      break;
    case 3:
      FUN__text__0040edd0(param_2,CONCAT22(uVar3,param_3));
      break;
    case 4:
      FUN__text__0040f0d0(param_2,CONCAT22(uVar2,param_3));
      break;
    case 5:
      FUN__text__0040f3e0(param_2,CONCAT22(uVar2,param_3));
      break;
    case 6:
      FUN__text__0040fc20(param_2,CONCAT22(uVar3,param_3));
      break;
    case 7:
      FUN__text__0040ff30(param_2,CONCAT22(uVar2,param_3));
      break;
    case 8:
      FUN__text__00410270(param_2,CONCAT22(uVar2,param_3));
    }
  }
  local_8 = 0x40e61e;
  FUN__text__0056ce80();
  return;
}

