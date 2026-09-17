
void __thiscall
FUN__text__00416af0(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

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
  local_8 = param_1;
  FUN__text__004077c0(param_1);
  *(undefined2 *)(param_2 + 0x58) = 0x80;
  FUN__text__00407870(param_3,param_4);
  *(undefined4 *)(param_2 + 0x5c) = 0;
  *(undefined1 *)(param_2 + 0x67) = 0xff;
  *(undefined1 *)(param_2 + 100) = 0x80;
  *(undefined1 *)(param_2 + 0x65) = 0x80;
  *(undefined1 *)(param_2 + 0x66) = 0x80;
  *(undefined2 *)(param_2 + 0x76) = 100;
  FUN__text__004079c0(0,0);
  local_8 = 0x416b7a;
  FUN__text__0056ce80();
  return;
}

