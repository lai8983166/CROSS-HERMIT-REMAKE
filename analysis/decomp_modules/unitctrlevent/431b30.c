
int FUN__text__00431b30(int param_1,int param_2)

{
  short *psVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  for (local_1c = 0; local_1c != 0x10; local_1c = local_1c + 1) {
    *(undefined2 *)(param_1 + 0x30 + local_1c * 0x32) = 0;
  }
  if (param_2 == 0) {
    local_14 = 4;
  }
  else {
    local_14 = 0x10;
  }
  for (local_1c = 0; local_1c != local_14; local_1c = local_1c + 1) {
    psVar1 = (short *)(param_1 + local_1c * 0x32);
    psVar1[0x18] = *psVar1 * 10 + psVar1[3] * 5 + psVar1[9] * 10 + psVar1[0xc] * 5 + psVar1[0xf];
  }
  for (local_1c = 0; local_1c != 0x10; local_1c = local_1c + 1) {
    *(undefined2 *)(param_1 + 800 + local_1c * 4) = (undefined2)local_1c;
    *(undefined2 *)(param_1 + 0x322 + local_1c * 4) = 0;
  }
  for (local_1c = 0; local_1c != 4; local_1c = local_1c + 1) {
    local_18 = (int)(char)(&DAT_007f44e4)[local_1c];
    *(short *)(param_1 + 0x322 + local_18 * 4) =
         *(short *)(param_1 + 0x322 + local_18 * 4) + *(short *)(param_1 + 0x30 + local_1c * 0x32);
  }
  return local_18;
}

