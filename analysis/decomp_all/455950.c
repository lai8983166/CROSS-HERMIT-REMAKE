
void __fastcall FUN__text__00455950(int param_1)

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
  local_c = *(int *)(param_1 + 0x60) + 0x2170;
  local_8 = param_1;
  iVar1 = FUN__text__00454c40();
  if ((iVar1 == 0) && (*(char *)(*(int *)(local_8 + 0x60) + 0x216c) != '\0')) {
    for (local_10 = 0; local_10 != 0x10; local_10 = local_10 + 1) {
      if ((*(char *)(local_c + local_10 * 0xc) != -1) &&
         (*(int *)(local_c + 8 + local_10 * 0xc) = *(int *)(local_c + 8 + local_10 * 0xc) + -1,
         *(int *)(local_c + 8 + local_10 * 0xc) == 0)) {
        iVar1 = FUN__text__004551c0((int)*(char *)(local_c + 1 + local_10 * 0xc),
                                    (int)*(short *)(local_c + 2 + local_10 * 0xc));
        if (iVar1 != 0) {
          FUN__text__00454980(0,(int)*(char *)(local_c + 1),(int)*(short *)(local_c + 2),0);
        }
        *(undefined4 *)(local_c + 8) = *(undefined4 *)(local_c + 4);
        break;
      }
    }
  }
  local_8 = 0x455a68;
  FUN__text__0056ce80();
  return;
}

