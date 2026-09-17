
void FUN__text__005466e2(int param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  
  if ((*(byte *)(param_1 + 0x10c) & 0x20) == 0) {
    if ((*(byte *)(param_1 + 0x5d) & 8) != 0) {
      return;
    }
  }
  else if ((*(uint *)(param_1 + 0x5c) & 0x300) == 0x300) {
    return;
  }
  uVar1 = FUN__text__0054cfe4(*(undefined4 *)(param_1 + 0x100),param_2,param_3);
  *(undefined4 *)(param_1 + 0x100) = uVar1;
  return;
}

