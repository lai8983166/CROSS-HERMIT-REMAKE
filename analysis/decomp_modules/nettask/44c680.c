
void __fastcall FUN__text__0044c680(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  short *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x1a54;
  local_10 = (short *)(param_1 + 0x1a88);
  local_8 = param_1;
  local_14 = FUN__text__0044c490((int)*local_10,*(undefined4 *)(param_1 + 0x1ba4));
  local_14 = FUN__text__0044c560((int)*local_10,(int)(char)local_10[1],
                                 *(undefined4 *)(local_8 + 0x1ba4));
  local_8 = 0x44c700;
  FUN__text__0056ce80();
  return;
}

