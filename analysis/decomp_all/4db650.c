
int FUN__text__004db650(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [16];
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 < param_2) {
    param_1 = param_2;
  }
  if (param_3 <= param_1) {
    param_1 = param_3;
  }
  return param_1;
}

