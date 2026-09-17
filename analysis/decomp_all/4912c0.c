
void __thiscall
FUN__text__004912c0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = (short)((int)((int)*(short *)(param_1 + 0x2a316) +
                          ((int)*(short *)(param_1 + 0x2a316) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (short)((int)((int)*(short *)(param_1 + 0x2a318) +
                          ((int)*(short *)(param_1 + 0x2a318) >> 0x1f & 0xfU)) >> 4);
  local_8 = param_1;
  iVar1 = FUN__text__0043c160((int)local_10,(int)local_14);
  if (iVar1 == 0) {
    *(undefined1 *)(local_8 + 0x30994) = 0;
    goto LAB__text__004913d0;
  }
  if (*(short *)(local_8 + 0x30992) == -1) {
    *(undefined1 *)(local_8 + 0x30994) = 0;
    goto LAB__text__004913d0;
  }
  local_c = local_8 + 0x80aec + *(short *)(local_8 + 0x30992) * 0x520;
  iVar1 = FUN__text__0046a250(param_4);
  if (iVar1 == 0) {
LAB__text__004913aa:
    iVar1 = FUN__text__0046a550(local_c);
    if (iVar1 == 0) {
      *(undefined1 *)(local_8 + 0x30994) = 0;
    }
    else {
      *(undefined1 *)(local_8 + 0x30994) = 1;
    }
  }
  else {
    iVar1 = FUN__text__0046a430(local_c);
    if (iVar1 == 0) {
      iVar1 = FUN__text__0046a5e0(local_c);
      if (iVar1 == 0) goto LAB__text__004913aa;
    }
    *(undefined1 *)(local_8 + 0x30994) = 2;
  }
LAB__text__004913d0:
  local_8 = 0x4913dd;
  FUN__text__0056ce80();
  return;
}

