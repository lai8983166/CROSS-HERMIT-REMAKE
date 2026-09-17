
void FUN__text1__0084dc59(undefined4 *param_1)

{
  if (((param_1[3] & 0x83) != 0) && ((param_1[3] & 8) != 0)) {
    FUN__text1__008497d3(param_1[2]);
    *(ushort *)(param_1 + 3) = *(ushort *)(param_1 + 3) & 0xfbf7;
    *param_1 = 0;
    param_1[2] = 0;
    param_1[1] = 0;
  }
  return;
}

