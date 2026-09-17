
bool __thiscall FUN__text__0041d8e0(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  bool bVar3;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  bVar3 = *(int *)(param_1 + 0xc) != 0;
  if (bVar3) {
    *(undefined4 *)(param_1 + 600) = param_2;
    *(undefined4 *)(param_1 + 0x25c) = param_3;
  }
  return !bVar3;
}

