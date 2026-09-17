
undefined4 __thiscall
FUN__text__004c1f40(int param_1,int param_2,undefined4 param_3,int param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(param_3) {
  case 0:
    *(undefined4 *)(param_1 + param_2 * 0x1c8 + 0x3c + param_4 * 4) = param_5;
    break;
  case 1:
    *(undefined4 *)(&DAT_007aab1c + param_4 * 4) = param_5;
    break;
  case 2:
  case 3:
    return 0;
  }
  return 1;
}

