
void __fastcall FUN__text__004a7c40(int param_1)

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
  *(undefined2 *)(param_1 + 0x7950) = 0;
  *(undefined2 *)(param_1 + 0x76c4) = 1;
  *(undefined2 *)(param_1 + 0x76c8) = 0;
  local_8 = param_1;
  FUN__text__00422360(8);
  FUN__text__00415420();
  *(undefined2 *)(local_8 + 0x76c6) = 2;
  *(undefined2 *)(local_8 + 0x30) = 0;
  do {
    *(undefined1 *)(local_8 + 0x76c2) = 0;
    DAT_007d6a26 = FUN__text__004a7d30();
    FUN__text__004a6f90();
    FUN__text__004a81a0();
    FUN__text__004a3240();
    FUN__text__00422360(0);
  } while (*(short *)(local_8 + 0x76c4) != 0);
  if (*(short *)(local_8 + 0x30) != 0) {
    FUN__text__004a1920();
  }
  local_8 = 0x4a7d22;
  FUN__text__0056ce80();
  return;
}

