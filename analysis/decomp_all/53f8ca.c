
void __thiscall FUN__text__0053f8ca(int param_1,uint param_2,undefined4 *param_3)

{
  if (((param_2 & 0x70000000) == 0x20000000) && ((param_2 & 0x2000) == 0)) {
    if (*(int *)(param_1 + 0xac) == 0) {
      *(int *)(param_1 + 0x9c) = *(int *)(param_1 + 0x9c) + 0x14;
      param_2 = param_2 & 0x1fff | 0x82000000;
    }
    else {
      *(int *)(param_1 + 0x9c) = *(int *)(param_1 + 0x9c) + 0x18;
      FUN__text__00548e1c(0x51);
      param_2 = param_2 | 0xf0000;
    }
    FUN__text__00548e1c(param_2);
    FUN__text__00548e1c(*param_3);
    FUN__text__00548e1c(param_3[1]);
    FUN__text__00548e1c(param_3[2]);
    FUN__text__00548e1c(param_3[3]);
  }
  else {
    FUN__text__0053eb92(param_1,"invalid constant");
    *(undefined4 *)(param_1 + 0x98) = 1;
  }
  return;
}

