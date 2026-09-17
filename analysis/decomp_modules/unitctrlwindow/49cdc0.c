
void FUN__text__0049cdc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0xde708) = 0;
  *(undefined1 *)(local_8 + 0xde716) = 0x80;
  *(undefined1 *)(local_8 + 0xde715) = 0x80;
  *(undefined1 *)(local_8 + 0xde714) = 0x80;
  *(undefined2 *)(local_8 + 0xde726) = 200;
  local_c = param_1;
  if (param_1 == 0) {
    FUN__text__00407870(0x5a,4);
  }
  else if (param_1 == 1) {
    FUN__text__00407870(0x5a,3);
  }
  FUN__text__004079c0(0,600);
  local_8 = 0x49ce83;
  FUN__text__0056ce80();
  return;
}

