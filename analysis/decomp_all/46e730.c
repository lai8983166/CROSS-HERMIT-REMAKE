
void __fastcall FUN__text__0046e730(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_10 = 0; local_10 != 5; local_10 = local_10 + 1) {
    *(undefined4 *)(param_1 + 0xdc8ec + local_10 * 0x3ec) = 0;
  }
  local_10 = 0;
  local_8 = param_1;
  do {
    if (local_10 == 0xfa) {
      local_8 = 0x46e9ad;
      FUN__text__0056ce80();
      return;
    }
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_10 * 0x520);
    if (iVar1 != 0) {
      iVar1 = FUN__text__00469480(local_8 + 0x80aec + local_10 * 0x520);
      if (iVar1 != 0) {
        local_c = (int *)(local_8 + 0xdc8ec);
        *(int *)(local_8 + 0xdc8f0 + *local_c * 4) = local_8 + 0x80aec + local_10 * 0x520;
        *local_c = *local_c + 1;
        iVar1 = FUN__text__0046a550(local_8 + 0x80aec + local_10 * 0x520);
        if (iVar1 != 0) {
          local_c = (int *)(local_8 + 0xdd0c4);
          *(int *)(local_8 + 0xdd0c8 + *local_c * 4) = local_8 + 0x80aec + local_10 * 0x520;
          *local_c = *local_c + 1;
        }
        iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_10 * 0x520);
        if (iVar1 != 0) {
          local_c = (int *)(local_8 + 0xdd4b0);
          *(int *)(local_8 + 0xdd4b4 + *local_c * 4) = local_8 + 0x80aec + local_10 * 0x520;
          *local_c = *local_c + 1;
        }
        iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_10 * 0x520);
        if (iVar1 == 0) {
          iVar1 = FUN__text__0046a5e0(local_8 + 0x80aec + local_10 * 0x520);
          if (iVar1 == 0) goto LAB__text__0046e944;
        }
        local_c = (int *)(local_8 + 0xdd89c);
        *(int *)(local_8 + 0xdd8a0 + *local_c * 4) = local_8 + 0x80aec + local_10 * 0x520;
        *local_c = *local_c + 1;
      }
LAB__text__0046e944:
      iVar1 = FUN__text__004695d0(local_8 + 0x80aec + local_10 * 0x520);
      if (iVar1 != 0) {
        local_c = (int *)(local_8 + 0xdccd8);
        *(int *)(local_8 + 0xdccdc + *local_c * 4) = local_8 + 0x80aec + local_10 * 0x520;
        *local_c = *local_c + 1;
      }
    }
    local_10 = local_10 + 1;
  } while( true );
}

