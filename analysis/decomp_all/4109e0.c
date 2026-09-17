
void __thiscall FUN__text__004109e0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == 0) {
    *(undefined4 *)(param_1 + 0x44) = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x44) = 1;
  }
  return;
}

