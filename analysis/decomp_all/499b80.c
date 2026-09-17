
void __fastcall FUN__text__00499b80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined1 local_10;
  char *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (char *)(param_1 + 0x30998);
  if (*local_c != '\0') {
    local_8 = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0xde908) = 8;
    FUN__text__00407870((int)*(short *)(&DAT_0061a014 + local_c[2] * 4),
                        (int)*(short *)(&PTR_DAT_0061a016 + local_c[2]));
    *(undefined4 *)(local_8 + 0xde90c) = 1;
    *(undefined2 *)(local_8 + 0xde926) = 100;
    local_10 = (undefined1)((uint)*(undefined4 *)(local_c + 8) >> 8);
    *(undefined1 *)(local_8 + 0xde917) = local_10;
    *(undefined1 *)(local_8 + 0xde914) = 0x80;
    *(undefined1 *)(local_8 + 0xde915) = 0x80;
    *(undefined1 *)(local_8 + 0xde916) = 0x80;
    FUN__text__004079c0((int)*(short *)(local_c + 0x10),(int)*(short *)(local_c + 0x12));
  }
  local_8 = 0x499c7f;
  FUN__text__0056ce80();
  return;
}

