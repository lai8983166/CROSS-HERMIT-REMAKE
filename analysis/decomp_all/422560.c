
void __thiscall FUN__text__00422560(int param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(uint *)(param_1 + 4) = *(uint *)(param_1 + 4) | param_2;
  return;
}

