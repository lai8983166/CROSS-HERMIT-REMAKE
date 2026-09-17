
bool __thiscall
FUN__text__0042bcb0(int param_1,undefined4 *param_2,undefined4 *param_3,undefined4 *param_4)

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
  bVar3 = *(int *)(param_1 + 4) == 0;
  if (!bVar3) {
    *param_2 = *(undefined4 *)(param_1 + 4);
    *param_3 = *(undefined4 *)(param_1 + 8);
    *param_4 = *(undefined4 *)(param_1 + 0xc);
  }
  return bVar3;
}

