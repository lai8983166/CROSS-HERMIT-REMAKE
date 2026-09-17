
void __fastcall FUN__text__00466880(int param_1)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    local_10 = local_8 + 0x10c680 + local_c * 0x520;
    uVar1 = FUN__text__0040a100(local_10 + 0x48);
    *(undefined1 *)(local_10 + 4) = uVar1;
    *(short *)(local_10 + 10) = *(short *)(local_10 + 10) + 1;
  }
  local_8 = 0x466904;
  FUN__text__0056ce80();
  return;
}

