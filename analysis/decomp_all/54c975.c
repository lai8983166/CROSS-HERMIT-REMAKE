
void FUN__text__0054c975(int param_1,int param_2,int param_3)

{
  if ((((*(uint *)(param_1 + 0x58) & 1) == 0) || ((*(uint *)(param_1 + 0x58) & 4) == 0)) &&
     (FUN__text__0054381d(param_1,"No image in file"), param_2 == 0)) {
    return;
  }
  *(uint *)(param_1 + 0x58) = *(uint *)(param_1 + 0x58) | 0x18;
  if (param_3 != 0) {
    FUN__text__0054383b(param_1,"Incorrect IEND chunk length");
  }
  FUN__text__0054c5c9(param_1,param_3);
  return;
}

