
void FUN__text__004a2700(short param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  short local_10;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  sVar1 = *(short *)(&DAT_007aa9ea + param_1 * 2);
  local_10 = 0;
  while ((local_10 < sVar1 &&
         ((uint)*(ushort *)(&DAT_007a5bcc + sVar1 * 10 + param_1 * 1000) != (int)param_1))) {
    local_10 = local_10 + 1;
  }
  for (; (int)local_10 < sVar1 + -1; local_10 = local_10 + 1) {
    (&DAT_007a5bca)[local_10 * 10 + param_1 * 1000] =
         (&DAT_007a5bca)[(local_10 + 1) * 10 + param_1 * 1000];
    (&DAT_007a5bcb)[local_10 * 10 + param_1 * 1000] =
         (&DAT_007a5bcb)[(local_10 + 1) * 10 + param_1 * 1000];
    *(undefined2 *)(&DAT_007a5bcc + local_10 * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bcc + (local_10 + -1) * 10 + param_1 * 1000);
    *(undefined2 *)(&DAT_007a5bce + local_10 * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bce + (local_10 + 1) * 10 + param_1 * 1000);
    *(undefined2 *)(&DAT_007a5bd0 + local_10 * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bd0 + (local_10 + 1) * 10 + param_1 * 1000);
  }
  *(short *)(&DAT_007aa9ea + param_1 * 2) = *(short *)(&DAT_007aa9ea + param_1 * 2) + -1;
  return;
}

