
void FUN__text__004b9340(uint param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_98 [16];
  undefined1 local_58 [76];
  undefined *local_c;
  undefined *local_8;
  
  puVar2 = local_98;
  for (iVar1 = 0x25; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = &DAT_007e17e8 + (param_1 & 0xffff) * 0x4a0;
  local_c = &DAT_007f4518 + (param_2 & 0xffff) * 0xb0;
  FUN__text__004b93c0(local_8,local_c,local_58);
  local_8 = (undefined *)0x4b93b0;
  FUN__text__0056ce80();
  return;
}

