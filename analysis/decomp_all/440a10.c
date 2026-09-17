
void __fastcall FUN__text__00440a10(int param_1)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  short local_18;
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = *(short *)(param_1 + 0x26544) << 1;
  local_8 = param_1;
  for (local_10 = 0; local_10 != *(short *)(local_8 + 0x26546); local_10 = local_10 + 1) {
    local_14 = *(int *)(local_8 + 0x2658c) + (int)local_10 * (int)local_18;
    local_c = 0;
    while( true ) {
      if (*(short *)(local_8 + 0x26544) <= local_c) break;
      uVar1 = FUN__text__00440af0(local_c,CONCAT22(local_c >> 0xf,local_10));
      *(undefined2 *)(local_14 + local_c * 2) = uVar1;
      *(undefined2 *)(local_14 + 2 + local_c * 2) = *(undefined2 *)(local_14 + local_c * 2);
      local_c = local_c + 2;
    }
  }
  local_8 = 0x440aea;
  FUN__text__0056ce80();
  return;
}

