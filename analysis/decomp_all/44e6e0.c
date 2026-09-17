
int __thiscall FUN__text__0044e6e0(int param_1,int param_2,short param_3,short param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [19];
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return (int)*(short *)(*(int *)(param_1 + 0xc4 + param_2 * 4) +
                        (*(int *)(param_1 + 0x40) * (int)param_4 + (int)param_3) * 2);
}

