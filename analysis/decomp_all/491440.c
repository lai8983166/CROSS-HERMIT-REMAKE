
void __fastcall FUN__text__00491440(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(short *)(param_1 + 0x30992) != -1) {
    local_c = param_1 + 0x80aec + *(short *)(param_1 + 0x30992) * 0x520;
    iVar1 = FUN__text__0046a550(local_c);
    if (iVar1 != 0) {
      *(undefined1 *)(local_8 + 0x30994) = 3;
      goto LAB__text__004914b3;
    }
  }
  *(undefined1 *)(local_8 + 0x30994) = 4;
LAB__text__004914b3:
  local_8 = 0x4914c0;
  FUN__text__0056ce80();
  return;
}

