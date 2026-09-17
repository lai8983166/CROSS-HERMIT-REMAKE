
uint __fastcall FUN__text__00467e00(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(int *)(param_1 + 0x2e710) = *(int *)(param_1 + 0x2e710) + 1;
  uVar1 = *(uint *)(param_1 + 0x2e70c);
  *(int *)(param_1 + 0x2e70c) = *(int *)(param_1 + 0x2e70c) * 0x48d159e1 + 1;
  return uVar1 >> 0x10 & 0x7fff;
}

