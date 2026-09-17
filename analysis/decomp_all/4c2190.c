
int __thiscall FUN__text__004c2190(int param_1,uint param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return *(int *)(param_1 + 0x14 + (param_2 & 0xffff) * 0x1c8) + (param_3 & 0xffff) * 0x30;
}

