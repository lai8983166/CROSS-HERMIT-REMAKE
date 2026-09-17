
void FUN__text__004cbf00(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                        undefined1 param_5,undefined1 param_6,undefined1 param_7,undefined1 param_8,
                        undefined2 param_9)

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
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined4 *)(param_1 + 0x5c) = param_4;
  *(undefined1 *)(param_1 + 0x67) = param_5;
  *(undefined1 *)(param_1 + 0x66) = param_6;
  *(undefined1 *)(param_1 + 0x65) = param_7;
  *(undefined1 *)(param_1 + 100) = param_8;
  *(undefined2 *)(param_1 + 0x76) = param_9;
  FUN__text__00408f90(param_2,param_3);
  local_8 = 0x4cbf88;
  FUN__text__0056ce80();
  return;
}

