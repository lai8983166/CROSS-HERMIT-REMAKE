
void FUN__text__004da5f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined2 *local_c;
  undefined2 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 < 200) {
    local_8 = &DAT_007e11b0;
    _memset(&DAT_007e11b0,0,0x30);
    iVar1 = param_1 * 0x4a0;
    local_c = (undefined2 *)(&DAT_006f5088 + iVar1);
    *local_8 = *local_c;
    local_8[1] = *(undefined2 *)(&DAT_006f508e + iVar1);
    *(undefined *)(local_8 + 2) = (&DAT_006f5090)[iVar1];
    *(undefined *)((int)local_8 + 5) = (&DAT_006f5094)[iVar1];
    *(undefined *)(local_8 + 3) = (&DAT_006f509c)[iVar1];
    *(undefined *)((int)local_8 + 7) = (&DAT_006f50a4)[iVar1];
    *(undefined *)(local_8 + 4) = (&DAT_006f50ac)[iVar1];
    *(undefined *)((int)local_8 + 9) = (&DAT_006f50b4)[iVar1];
    *(undefined *)(local_8 + 5) = (&DAT_006f50bc)[iVar1];
    *(undefined *)((int)local_8 + 0xb) = (&DAT_006f50c4)[iVar1];
    if (param_1 < 0x40) {
      *(undefined *)(local_8 + 6) = (&DAT_006f50d8)[iVar1];
    }
    else {
      *(undefined *)(local_8 + 6) = (&DAT_006f50d8)[iVar1];
    }
    *(undefined *)(local_8 + 0x17) = (&DAT_006f50fa)[iVar1];
  }
  local_8 = (undefined2 *)0x4da708;
  FUN__text__0056ce80();
  return;
}

