
void FUN__text__004075e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058eb49;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00403620();
  local_8 = 0;
  FUN__text__00408c00();
  *(undefined4 *)(local_14 + 0x4c) = 0;
  *(undefined4 *)(local_14 + 0x48) = 0;
  *(undefined1 *)(local_14 + 0x67) = 0xff;
  *(undefined1 *)(local_14 + 100) = 0x80;
  *(undefined1 *)(local_14 + 0x65) = 0x80;
  *(undefined1 *)(local_14 + 0x66) = 0x80;
  *(undefined2 *)(local_14 + 0x58) = 0;
  *(undefined4 *)(local_14 + 0x5c) = 0;
  *(undefined4 *)(local_14 + 0x60) = 0;
  *(undefined4 *)(local_14 + 0x6c) = 0;
  *(undefined4 *)(local_14 + 0x68) = 0;
  *(undefined2 *)(local_14 + 0x72) = 100;
  *(undefined2 *)(local_14 + 0x70) = 100;
  *(undefined4 *)(local_14 + 0x54) = 0;
  *(undefined4 *)(local_14 + 0x50) = 0;
  *(undefined2 *)(local_14 + 0x74) = 0;
  *(undefined2 *)(local_14 + 0x76) = 0;
  *(undefined2 *)(local_14 + 0x78) = 0;
  *(undefined2 *)(local_14 + 0x7a) = 0;
  *(undefined2 *)(local_14 + 0x7c) = 0;
  *(undefined2 *)(local_14 + 0x7e) = 0;
  ExceptionList = local_10;
  local_8 = 0x40770a;
  FUN__text__0056ce80();
  return;
}

