
void __fastcall FUN__text__00441170(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = (int)*(short *)(param_1 + 0x265a6);
  local_8 = param_1;
  local_c = __ftol();
  local_20 = (int)*(short *)(local_8 + 0x265a8);
  local_10 = __ftol();
  local_c = local_c + *(short *)(local_8 + 0x2646c);
  local_10 = local_10 + *(short *)(local_8 + 0x26470);
  local_14 = __ftol();
  local_18 = __ftol();
  FUN__text__00410680((int)local_c,(int)local_10,(int)local_c + (int)local_14,
                      (int)local_10 + (int)local_18,0xc5,0xffffffff,1);
  local_8 = 0x44126c;
  FUN__text__0056ce80();
  return;
}

