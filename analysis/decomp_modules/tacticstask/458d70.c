
void __fastcall FUN__text__00458d70(int param_1)

{
  int iVar1;
  byte bVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  byte local_10;
  undefined3 uStack_f;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x30b28;
  local_8 = param_1;
  iVar1 = FUN__text__00454c40();
  if (iVar1 != 0) {
    FUN__text__00458f10();
  }
  bVar2 = (byte)((uint)*(undefined4 *)(local_c + 8) >> 8);
  _local_10 = CONCAT31(uStack_f,bVar2);
  FUN__text__00410310(0,0,0x400,0x300,0x65,bVar2 / 2 << 0x18,1);
  *(undefined1 *)(local_8 + 0x11804c) = 1;
  FUN__text__00499910();
  local_8 = 0x458e23;
  FUN__text__0056ce80();
  return;
}

