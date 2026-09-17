
void FUN__text__004a28d0(short param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  while ((local_10 < *(short *)(&DAT_007aa9ea + param_1 * 2) &&
         ((uint)*(ushort *)
                 (&DAT_007a5bcc + *(short *)(&DAT_007aa9ea + param_1 * 2) * 10 + param_1 * 1000) !=
          (int)param_1))) {
    local_10 = local_10 + 1;
  }
  return;
}

