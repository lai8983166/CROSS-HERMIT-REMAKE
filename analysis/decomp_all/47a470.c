
void FUN__text__0047a470(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0047cc90(param_1);
  if (iVar1 != 0) {
    local_c = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
    local_10 = FUN__text__0047ce70(param_1,local_c);
    if (local_10 != 0) {
      iVar1 = FUN__text__00468d80(param_1);
      if (iVar1 == 0) {
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xa0) = 0;
      }
      goto LAB__text__0047a51d;
    }
  }
  if (*(char *)(*(int *)(param_1 + 600) + 0xa0) != '\x04') {
    FUN__text__00475270(param_1,0xf);
  }
LAB__text__0047a51d:
  local_8 = 0x47a52a;
  FUN__text__0056ce80();
  return;
}

