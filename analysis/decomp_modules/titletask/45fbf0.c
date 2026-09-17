
void FUN__text__0045fbf0(undefined4 param_1,undefined4 param_2)

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
  *(undefined2 *)(local_8 + 0x90) = 0xc0;
  FUN__text__00407870(0x5a,6);
  *(undefined4 *)(local_8 + 0x94) = 0;
  *(undefined1 *)(local_8 + 0x9f) = 0xff;
  *(undefined1 *)(local_8 + 0x9c) = 0x80;
  *(undefined1 *)(local_8 + 0x9d) = 0x80;
  *(undefined1 *)(local_8 + 0x9e) = 0x80;
  *(undefined2 *)(local_8 + 0xae) = 0x5b;
  *(undefined2 *)(local_8 + 0x70) = 0x10e;
  *(undefined2 *)(local_8 + 0x72) = 0x5b;
  *(undefined2 *)(local_8 + 0xb0) = 0;
  *(undefined2 *)(local_8 + 0xb2) = 0;
  *(undefined2 *)(local_8 + 0xb4) = *(undefined2 *)(local_8 + 0x70);
  *(undefined2 *)(local_8 + 0xb6) = *(undefined2 *)(local_8 + 0x72);
  FUN__text__004079c0(param_1,param_2);
  local_8 = 0x45fce6;
  FUN__text__0056ce80();
  return;
}

