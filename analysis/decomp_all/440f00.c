
void FUN__text__00440f00(undefined2 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00440a10();
  FUN__text__00440c10();
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x26582) = param_1;
  FUN__text__004079c0(*(undefined4 *)(local_8 + 0x2646c),*(undefined4 *)(local_8 + 0x26470));
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x26502) = param_1;
  FUN__text__004079c0(*(undefined4 *)(local_8 + 0x2646c),*(undefined4 *)(local_8 + 0x26470));
  FUN__text__00441170();
  local_8 = 0x440fcd;
  FUN__text__0056ce80();
  return;
}

