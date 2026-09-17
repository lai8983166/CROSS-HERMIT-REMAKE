
void __fastcall FUN__text__004485b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 7;
  local_10 = 0x2ba;
  local_8 = param_1;
  FUN__text__00426820(DAT_007a49fc,7,0x2ba,0x12,0,param_1 + 0xdb8,param_1 + 0xe44,0x54);
  FUN__text__00425620(7,0x1de,0x23e,0x14,0x55);
  local_8 = 0x44863f;
  FUN__text__0056ce80();
  return;
}

