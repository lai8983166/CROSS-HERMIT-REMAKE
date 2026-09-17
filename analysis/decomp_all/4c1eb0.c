
int __thiscall FUN__text__004c1eb0(int param_1,int param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(param_3) {
  case 0:
    local_c = *(int *)(param_1 + param_2 * 0x1c8 + 0x3c + param_4 * 4);
    break;
  case 1:
    local_c = *(int *)(&DAT_007aab1c + param_4 * 4);
    break;
  case 2:
    local_c = param_4;
    break;
  case 3:
    local_c = -1;
  }
  return local_c;
}

