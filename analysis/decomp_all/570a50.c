
void FUN__text__00570a50(int param_1)

{
  code *pcVar1;
  int iVar2;
  int local_8;
  
  if (param_1 != 0) {
    for (local_8 = 0; local_8 < 5; local_8 = local_8 + 1) {
      iVar2 = FUN__text__00573780(0,0,0,0,"%ld bytes in %ld %hs Blocks.\n",
                                  *(undefined4 *)(param_1 + 0x18 + local_8 * 4),
                                  *(undefined4 *)(param_1 + 4 + local_8 * 4),
                                  (&PTR_DAT_007619d0)[local_8]);
      if (iVar2 == 1) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    iVar2 = FUN__text__00573780(0,0,0,0,"Largest number used: %ld bytes.\n",
                                *(undefined4 *)(param_1 + 0x2c));
    if (iVar2 == 1) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    iVar2 = FUN__text__00573780(0,0,0,0,"Total allocations: %ld bytes.\n",
                                *(undefined4 *)(param_1 + 0x30));
    if (iVar2 == 1) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  return;
}

