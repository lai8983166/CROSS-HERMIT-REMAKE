
undefined4 __thiscall FUN__text__00440d40(int param_1,short param_2,short param_3)

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
  if ((int)param_3 < *(int *)(param_1 + 0x26470)) {
    uVar1 = 0;
  }
  else if (*(int *)(param_1 + 0x26470) + *(int *)(param_1 + 0x26478) < (int)param_3) {
    uVar1 = 0;
  }
  else if ((int)param_2 < *(int *)(param_1 + 0x2646c)) {
    uVar1 = 0;
  }
  else if (*(int *)(param_1 + 0x2646c) + *(int *)(param_1 + 0x26474) < (int)param_2) {
    uVar1 = 0;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}

