
void __fastcall FUN__text__00455560(int param_1)

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
  local_c = *(int *)(param_1 + 0x60) + 0x20ec;
  local_8 = param_1;
  iVar1 = FUN__text__00454c40();
  if ((iVar1 == 0) && (*(char *)(*(int *)(local_8 + 0x60) + 0x20e8) != '\0')) {
    for (local_10 = 0; local_10 != 0x10; local_10 = local_10 + 1) {
      if ((*(char *)(local_c + local_10 * 8) != -1) &&
         (*(int *)(local_c + 4 + local_10 * 8) = *(int *)(local_c + 4 + local_10 * 8) + -1,
         *(int *)(local_c + 4 + local_10 * 8) < 1)) {
        iVar1 = FUN__text__004551c0((int)*(char *)(local_c + 1 + local_10 * 8),
                                    (int)*(short *)(local_c + 2 + local_10 * 8));
        if (iVar1 != 0) {
          FUN__text__00454980(0,(int)*(char *)(local_c + 1 + local_10 * 8),
                              (int)*(short *)(local_c + 2 + local_10 * 8),0);
        }
        FUN__text__00455390(local_c + local_10 * 8);
        break;
      }
    }
  }
  local_8 = 0x455674;
  FUN__text__0056ce80();
  return;
}

