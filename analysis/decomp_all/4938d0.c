
undefined1 * __fastcall FUN__text__004938d0(int param_1)

{
  undefined1 *puVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  puVar1 = (undefined1 *)(param_1 + 0x116254 + *(int *)(param_1 + 0x116250) * 0x524);
  *puVar1 = 1;
  puVar1[1] = 0;
  *(undefined2 *)(puVar1 + 2) = 300;
  *(int *)(param_1 + 0x116250) = *(int *)(param_1 + 0x116250) + 1;
  if (4 < *(int *)(param_1 + 0x116250)) {
    *(undefined4 *)(param_1 + 0x116250) = 0;
  }
  return puVar1;
}

