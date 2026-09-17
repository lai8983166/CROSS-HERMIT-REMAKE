
void FUN__text__0054cd70(int param_1,int param_2,undefined4 param_3)

{
  FUN__text__0054bd71(param_1,(byte *)(param_1 + 0x10c));
  if (((*(byte *)(param_1 + 0x10c) & 0x20) == 0) &&
     (FUN__text__00543850(param_1,"unknown critical chunk"), param_2 == 0)) {
    return;
  }
  if ((*(uint *)(param_1 + 0x58) & 4) != 0) {
    *(uint *)(param_1 + 0x58) = *(uint *)(param_1 + 0x58) | 8;
  }
  FUN__text__0054c5c9(param_1,param_3);
  return;
}

