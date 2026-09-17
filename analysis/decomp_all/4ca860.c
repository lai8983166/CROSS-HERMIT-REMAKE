
void __fastcall FUN__text__004ca860(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  undefined1 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 0x4c) == 1) {
    local_c = 1;
    local_10 = 0xff;
    local_14 = *(short *)(param_1 + 0x56) - *(short *)(param_1 + 0xa0) / 2;
    local_18 = *(short *)(param_1 + 0x58) - *(short *)(param_1 + 0xa2) / 2;
    local_8 = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined4 *)(local_8 + 0xbc) = local_c;
    *(undefined1 *)(local_8 + 199) = local_10;
    *(undefined1 *)(local_8 + 0xc6) = 0xff;
    *(undefined1 *)(local_8 + 0xc5) = 0xff;
    *(undefined1 *)(local_8 + 0xc4) = 0xff;
    *(undefined2 *)(local_8 + 0xd6) = 0x35;
    FUN__text__00408f90((int)local_14,(int)local_18);
  }
  local_8 = 0x4ca954;
  FUN__text__0056ce80();
  return;
}

