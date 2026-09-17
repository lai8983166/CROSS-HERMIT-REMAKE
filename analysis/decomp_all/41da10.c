
undefined4 __thiscall FUN__text__0041da10(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [17];
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x10) == 0) {
    uVar1 = 1;
  }
  else if ((param_2 < -5000) && (param_2 < 1)) {
    uVar1 = 1;
  }
  else {
    *(int *)(param_1 + 0x24c) = param_2;
    *(int *)(param_1 + 0x250) = param_2;
    uVar1 = 0;
  }
  return uVar1;
}

