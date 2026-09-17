
int FUN__text__00420b00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 0x1c) == 8) {
    param_1 = param_1 + 0x36;
  }
  else {
    param_1 = 0;
  }
  return param_1;
}

