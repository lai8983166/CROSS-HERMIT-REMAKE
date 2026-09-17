
void __thiscall
FUN__text__00401000(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

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
  local_8 = param_1;
  FUN__text__0056cd90(param_1,param_2);
  *(undefined4 *)(local_8 + 0x50) = param_3;
  *(undefined4 *)(local_8 + 0x54) = param_4;
  *(undefined4 *)(local_8 + 0x58) = 0;
  *(undefined4 *)(local_8 + 0x5c) = 0;
  *(undefined4 *)(local_8 + 0x60) = 0;
  *(undefined4 *)(local_8 + 0x670) = 0;
  *(undefined4 *)(local_8 + 0x674) = 0;
  local_8 = 0x401087;
  FUN__text__0056ce80();
  return;
}

