
void FUN__text__004610f0(undefined4 param_1)

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
  *(undefined2 *)(local_8 + 0x90) = 0x80;
  *(undefined4 *)(local_8 + 0x94) = 0;
  *(undefined1 *)(local_8 + 0x9f) = 0xff;
  *(undefined1 *)(local_8 + 0x9c) = 0x80;
  *(undefined1 *)(local_8 + 0x9d) = 0x80;
  *(undefined1 *)(local_8 + 0x9e) = 0x80;
  *(undefined2 *)(local_8 + 0xae) = 100;
  FUN__text__00407870(0x5a,param_1);
  FUN__text__004079c0(0,0);
  local_8 = 0x461198;
  FUN__text__0056ce80();
  return;
}

