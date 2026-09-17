
void __fastcall FUN__text__0046e520(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0xdc30c) = 0;
  local_8 = param_1;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (((iVar1 != 0) &&
        (iVar1 = FUN__text__00469480(local_8 + 0x80aec + local_c * 0x520), iVar1 != 0)) &&
       (local_14 = FUN__text__0046b130((int)(short)((uint)*(undefined4 *)
                                                           (local_8 + 0x80dd8 + local_c * 0x520) >>
                                                   0x10) - (int)*(short *)(local_8 + 0x2a30e),
                                       ((int)(short)((uint)*(undefined4 *)
                                                            (local_8 + 0x80ddc + local_c * 0x520) >>
                                                    0x10) - (int)*(short *)(local_8 + 0x2a310)) +
                                       0x1e), local_14 != 0)) {
      *(int *)(local_8 + 0xdc310 + *(int *)(local_8 + 0xdc30c) * 4) =
           local_8 + 0x80aec + local_c * 0x520;
      *(int *)(local_8 + 0xdc30c) = *(int *)(local_8 + 0xdc30c) + 1;
    }
  }
  if (1 < *(int *)(local_8 + 0xdc30c)) {
    for (local_10 = 0; iVar1 = local_10, local_10 != *(int *)(local_8 + 0xdc30c) + -1;
        local_10 = local_10 + 1) {
      while (local_c = iVar1 + 1, local_c != *(int *)(local_8 + 0xdc30c)) {
        iVar1 = local_c;
        if (*(int *)(*(int *)(local_8 + 0xdc310 + local_10 * 4) + 0x2f0) <
            *(int *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x2f0)) {
          local_18 = *(undefined4 *)(local_8 + 0xdc310 + local_10 * 4);
          *(undefined4 *)(local_8 + 0xdc310 + local_10 * 4) =
               *(undefined4 *)(local_8 + 0xdc310 + local_c * 4);
          *(undefined4 *)(local_8 + 0xdc310 + local_c * 4) = local_18;
        }
      }
    }
  }
  local_8 = 0x46e720;
  FUN__text__0056ce80();
  return;
}

