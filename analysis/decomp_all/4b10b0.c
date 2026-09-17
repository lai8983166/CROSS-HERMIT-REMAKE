
void FUN__text__004b10b0(undefined4 param_1,uint param_2)

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
  FUN__text__004d5ec0(param_1,(param_2 & 0xffff) * 0x24 + 0x16f,0x1bf,0x23,0x23);
  local_8 = 0x4b1102;
  FUN__text__0056ce80();
  return;
}

