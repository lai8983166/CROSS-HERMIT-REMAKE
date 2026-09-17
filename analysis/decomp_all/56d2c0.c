
undefined4 FUN__text__0056d2c0(int param_1,int param_2,undefined4 param_3)

{
  undefined4 uVar1;
  
  if ((*(uint *)(param_1 + 4) & 0x66) != 0) {
    *(undefined4 *)(param_2 + 0x24) = 1;
    return 1;
  }
  FUN__text__00574620(param_1,*(undefined4 *)(param_2 + 0xc),param_3,0,*(undefined4 *)(param_2 + 8),
                      *(undefined4 *)(param_2 + 0x10),*(undefined4 *)(param_2 + 0x14),1);
  if (*(int *)(param_2 + 0x24) == 0) {
    FUN__text__0056d070(param_2,param_1);
  }
                    /* WARNING: Could not recover jumptable at 0x0056d334. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar1 = (**(code **)(param_2 + 0x18))();
  return uVar1;
}

