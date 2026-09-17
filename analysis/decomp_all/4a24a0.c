
void FUN__text__004a24a0(short param_1,short param_2)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [17];
  short local_10;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  sVar1 = *(short *)(&DAT_007aa9ea + param_1 * 2);
  for (local_10 = 0; local_10 < sVar1; local_10 = local_10 + 1) {
    (&DAT_007a5bca)[((int)sVar1 - (int)local_10) * 10 + param_1 * 1000] =
         (&DAT_007a5bca)[(((int)sVar1 - (int)local_10) + -1) * 10 + param_1 * 1000];
    (&DAT_007a5bcb)[((int)sVar1 - (int)local_10) * 10 + param_1 * 1000] =
         (&DAT_007a5bcb)[(((int)sVar1 - (int)local_10) + -1) * 10 + param_1 * 1000];
    *(undefined2 *)(&DAT_007a5bcc + ((int)sVar1 - (int)local_10) * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bcc + (((int)sVar1 - (int)local_10) + -1) * 10 + param_1 * 1000);
    *(undefined2 *)(&DAT_007a5bce + ((int)sVar1 - (int)local_10) * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bce + (((int)sVar1 - (int)local_10) + -1) * 10 + param_1 * 1000);
    *(undefined2 *)(&DAT_007a5bd0 + ((int)sVar1 - (int)local_10) * 10 + param_1 * 1000) =
         *(undefined2 *)(&DAT_007a5bd0 + (((int)sVar1 - (int)local_10) + -1) * 10 + param_1 * 1000);
  }
  (&DAT_007a5bca)[param_1 * 1000] = 1;
  (&DAT_007a5bcb)[param_1 * 1000] = 0;
  *(short *)(&DAT_007a5bcc + param_1 * 1000) = param_2;
  *(undefined2 *)(&DAT_007a5bce + param_1 * 1000) = *(undefined2 *)(&DAT_0074bed4 + param_2 * 0x60);
  *(undefined2 *)(&DAT_007a5bd0 + param_1 * 1000) = 0;
  *(short *)(&DAT_007aa9ea + param_1 * 2) = *(short *)(&DAT_007aa9ea + param_1 * 2) + 1;
  return;
}

