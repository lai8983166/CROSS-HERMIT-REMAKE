
uint FUN__text1__0083dd1c(int param_1)

{
  uint uVar1;
  uint3 uVar4;
  uint uVar2;
  uint uVar3;
  uint uVar5;
  
  param_1 = param_1 + *(int *)(param_1 + 0x3c);
  uVar5 = param_1 + 0x18;
  uVar4 = (uint3)((uint)(param_1 + 4) >> 8);
  if (*(short *)(param_1 + 6) == 3) {
    if (*(int *)(param_1 + 0x78) == 0) {
      uVar1 = *(uint *)(param_1 + 0x154);
      uVar3 = uVar1 + *(int *)(param_1 + 0x150);
      uVar2 = uVar3;
      if ((*(uint *)(param_1 + 0xa0) < uVar1) || (uVar2 = uVar5, uVar3 <= *(uint *)(param_1 + 0xa0))
         ) {
        uVar2 = uVar2 & 0xffffff00;
      }
      else if ((*(uint *)(param_1 + 0x80) < uVar1) || (uVar3 <= *(uint *)(param_1 + 0x80))) {
        uVar2 = *(uint *)(param_1 + 0x80) & 0xffffff00;
      }
      else if ((*(uint *)(param_1 + 0x88) < uVar1) ||
              (uVar5 = *(uint *)(param_1 + 0x88), uVar3 <= uVar5)) {
        uVar2 = uVar5 & 0xffffff00;
      }
      else {
        uVar4 = (uint3)(uVar5 >> 8);
        if (*(int *)(param_1 + 0x108) == 0) {
          if (*(uint *)(param_1 + 0x158) < 0x1001) {
            uVar2 = CONCAT31(uVar4,1);
          }
          else {
            uVar2 = (uint)uVar4 << 8;
          }
        }
        else {
          uVar2 = (uint)uVar4 << 8;
        }
      }
    }
    else {
      uVar2 = (uint)uVar4 << 8;
    }
  }
  else {
    uVar2 = (uint)uVar4 << 8;
  }
  return uVar2;
}

