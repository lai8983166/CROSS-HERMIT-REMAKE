
void FUN__text__0054bd71(undefined4 param_1,byte *param_2)

{
  byte bVar1;
  
  bVar1 = *param_2;
  if (((((((bVar1 < 0x29) || (0x7a < bVar1)) || ((0x5a < bVar1 && (bVar1 < 0x61)))) ||
        ((bVar1 = param_2[1], bVar1 < 0x29 || (0x7a < bVar1)))) ||
       ((0x5a < bVar1 && (bVar1 < 0x61)))) ||
      ((((bVar1 = param_2[2], bVar1 < 0x29 || (0x7a < bVar1)) || ((0x5a < bVar1 && (bVar1 < 0x61))))
       || ((bVar1 = param_2[3], bVar1 < 0x29 || (0x7a < bVar1)))))) ||
     ((0x5a < bVar1 && (bVar1 < 0x61)))) {
    FUN__text__00543850(param_1,"invalid chunk type");
  }
  return;
}

