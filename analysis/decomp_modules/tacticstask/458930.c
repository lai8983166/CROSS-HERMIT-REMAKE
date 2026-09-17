
void FUN__text__00458930(undefined4 param_1,undefined4 param_2)

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
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x148) = 0xc0;
  FUN__text__00407870(0x5a,7);
  *(undefined4 *)(local_8 + 0x14c) = 0;
  *(undefined1 *)(local_8 + 0x157) = 0xff;
  *(undefined1 *)(local_8 + 0x154) = 0x80;
  *(undefined1 *)(local_8 + 0x155) = 0x80;
  *(undefined1 *)(local_8 + 0x156) = 0x80;
  *(undefined2 *)(local_8 + 0x166) = 4;
  *(undefined2 *)(local_8 + 0x128) = 0x10e;
  *(undefined2 *)(local_8 + 0x12a) = 0x5b;
  *(undefined2 *)(local_8 + 0x168) = 0;
  *(undefined2 *)(local_8 + 0x16a) = 0;
  *(undefined2 *)(local_8 + 0x16c) = *(undefined2 *)(local_8 + 0x128);
  *(undefined2 *)(local_8 + 0x16e) = *(undefined2 *)(local_8 + 0x12a);
  FUN__text__004079c0(param_1,param_2);
  local_8 = 0x458a3b;
  FUN__text__0056ce80();
  return;
}

