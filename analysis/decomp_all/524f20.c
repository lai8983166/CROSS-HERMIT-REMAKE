
void __fastcall FUN__text__00524f20(int param_1)

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
  if (*(char *)(param_1 + 0x38) != '\0') {
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0x238) = 0;
    *(undefined4 *)(local_8 + 0x23c) = 0;
    *(undefined1 *)(local_8 + 0x247) = 0xff;
    *(undefined1 *)(local_8 + 0x246) = 0x66;
    *(undefined1 *)(local_8 + 0x245) = 0x66;
    *(undefined1 *)(local_8 + 0x244) = 0x66;
    FUN__text__0040a100(local_8 + 0x5a8);
  }
  if (*(char *)(local_8 + 0x142) != '\0') {
    FUN__text__0040a330(local_8 + 0x5a8,local_8 + 0x1e0,0x200,(int)*(short *)(local_8 + 0x14c),0xb4)
    ;
  }
  if (*(char *)(local_8 + 0x143) != '\0') {
    FUN__text__0040a330(local_8 + 0x5a8,local_8 + 0x1e0,0x200,(int)*(short *)(local_8 + 0x14e),0xb4)
    ;
  }
  local_8 = 0x52504d;
  FUN__text__0056ce80();
  return;
}

