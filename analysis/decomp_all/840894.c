
undefined4 FUN__text1__00840894(int param_1,int param_2,char *param_3,int param_4)

{
  undefined4 uVar1;
  
  if (((param_3 == (char *)0x0) || (*param_3 != s_1_1_4_0086edb4[0])) || (param_4 != 0x38)) {
    uVar1 = 0xfffffffa;
  }
  else if (param_1 == 0) {
    uVar1 = 0xfffffffe;
  }
  else {
    *(undefined4 *)(param_1 + 0x18) = 0;
    if (*(int *)(param_1 + 0x20) == 0) {
      *(code **)(param_1 + 0x20) = FUN__text1__0084153e;
      *(undefined4 *)(param_1 + 0x28) = 0;
    }
    if (*(int *)(param_1 + 0x24) == 0) {
      *(code **)(param_1 + 0x24) = FUN__text1__00841567;
    }
    uVar1 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),1,0x18);
    *(undefined4 *)(param_1 + 0x1c) = uVar1;
    if (*(int *)(param_1 + 0x1c) == 0) {
      uVar1 = 0xfffffffc;
    }
    else {
      *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14) = 0;
      *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0xc) = 0;
      if (param_2 < 0) {
        param_2 = -param_2;
        *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0xc) = 1;
      }
      if ((param_2 < 8) || (0xf < param_2)) {
        FUN__text1__0084082b(param_1);
        uVar1 = 0xfffffffe;
      }
      else {
        *(int *)(*(int *)(param_1 + 0x1c) + 0x10) = param_2;
        uVar1 = FUN__text1__00844cb7
                          (param_1,~-(uint)(*(int *)(*(int *)(param_1 + 0x1c) + 0xc) != 0) &
                                   0x841580,1 << ((byte)param_2 & 0x1f));
        *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14) = uVar1;
        if (*(int *)(*(int *)(param_1 + 0x1c) + 0x14) == 0) {
          FUN__text1__0084082b(param_1);
          uVar1 = 0xfffffffc;
        }
        else {
          FUN__text1__008407c0(param_1);
          uVar1 = 0;
        }
      }
    }
  }
  return uVar1;
}

