
void FUN__text__004902a0(void *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_1,0,0x10);
  local_8 = 0x4902da;
  FUN__text__0056ce80();
  return;
}

