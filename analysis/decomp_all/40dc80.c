
bool __fastcall FUN__text__0040dc80(int param_1)

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
  bVar3 = *(int *)(param_1 + 0x14) != 0;
  if (bVar3) {
    *(undefined4 *)(param_1 + 0x30) = *(undefined4 *)(param_1 + 0x14);
    *(undefined4 *)(param_1 + 0x2c) = 0;
  }
  return !bVar3;
}

