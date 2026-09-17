
undefined4 FUN__text__0054b625(int param_1,int param_2,char *param_3,int param_4)

{
  int iVar1;
  undefined4 uVar2;
  
  if (((param_3 == (char *)0x0) || (*param_3 != '1')) || (param_4 != 0x38)) {
    uVar2 = 0xfffffffa;
  }
  else if (param_1 == 0) {
    uVar2 = 0xfffffffe;
  }
  else {
    *(undefined4 *)(param_1 + 0x18) = 0;
    if (*(int *)(param_1 + 0x20) == 0) {
      *(code **)(param_1 + 0x20) = FUN__text__0055d4f0;
      *(undefined4 *)(param_1 + 0x28) = 0;
    }
    if (*(int *)(param_1 + 0x24) == 0) {
      *(undefined1 **)(param_1 + 0x24) = &LAB__text__0055d500;
    }
    iVar1 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),1,0x18);
    *(int *)(param_1 + 0x1c) = iVar1;
    if (iVar1 == 0) {
      uVar2 = 0xfffffffc;
    }
    else {
      *(undefined4 *)(iVar1 + 0x14) = 0;
      *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0xc) = 0;
      if (param_2 < 0) {
        param_2 = -param_2;
        *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0xc) = 1;
      }
      if ((param_2 < 8) || (0xf < param_2)) {
        uVar2 = 0xfffffffe;
      }
      else {
        *(int *)(*(int *)(param_1 + 0x1c) + 0x10) = param_2;
        uVar2 = FUN__text__0055cb26(param_1,~-(uint)(*(int *)(*(int *)(param_1 + 0x1c) + 0xc) != 0)
                                            & 0x55d3c0,1 << ((byte)param_2 & 0x1f));
        *(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14) = uVar2;
        if (*(int *)(*(int *)(param_1 + 0x1c) + 0x14) != 0) {
          FUN__text__0054b5a8(param_1);
          return 0;
        }
        uVar2 = 0xfffffffc;
      }
      FUN__text__0054b5e7(param_1);
    }
  }
  return uVar2;
}

