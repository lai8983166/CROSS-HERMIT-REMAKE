
void FUN__text__00459450(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  while( true ) {
    FUN__text__0040ec50(200,200,1,0xffffffff,0,"SPACE : GO TACTICS");
    FUN__text__0040ec50(200,0xd8,1,0xffffffff,0,"ENTER : SET RESULT TO TACTICS-RESULT");
    FUN__text__0040ec50(200,300,1,0xffffffff,0,(&PTR_s_Perfect_0060cd50)[local_10]);
    FUN__text__00422360(0);
    iVar1 = FUN__text__004128f0(200,1);
    if (iVar1 != 0) {
      local_10 = local_10 + 1;
    }
    iVar1 = FUN__text__004128f0(0xd0,1);
    if (iVar1 != 0) {
      local_10 = local_10 + -1;
    }
    if (local_10 < 0) {
      local_10 = 0;
    }
    if (4 < local_10) {
      local_10 = 4;
    }
    iVar1 = FUN__text__004128f0(0x1c,1);
    if (iVar1 != 0) break;
    iVar1 = FUN__text__004128f0(0x39,1);
    if (iVar1 != 0) goto LAB__text__0045963e;
  }
  DAT_007f450c = (short)local_10 + 1;
  DAT_007f450e = 0;
  DAT_007f4510 = 1;
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    (&DAT_007f44be)[local_c] = 0;
  }
  for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
    *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0) = 0;
    *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0) = 0;
    (&DAT_007f45c6)[local_c * 0xb0] = 0;
  }
LAB__text__0045963e:
  local_8 = 0x45964b;
  FUN__text__0056ce80();
  return;
}

