
uint FUN__text1__0083eee5(int param_1)

{
  int iVar1;
  uint uVar2;
  
  if ((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) {
    uVar2 = 0xfffffffe;
  }
  else {
    iVar1 = *(int *)(*(int *)(param_1 + 0x1c) + 4);
    if ((iVar1 == 0x2a) || ((iVar1 == 0x71 || (iVar1 == 0x29a)))) {
      if (*(int *)(*(int *)(param_1 + 0x1c) + 8) != 0) {
        (**(code **)(param_1 + 0x24))
                  (*(undefined4 *)(param_1 + 0x28),*(undefined4 *)(*(int *)(param_1 + 0x1c) + 8));
      }
      if (*(int *)(*(int *)(param_1 + 0x1c) + 0x3c) != 0) {
        (**(code **)(param_1 + 0x24))
                  (*(undefined4 *)(param_1 + 0x28),*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x3c))
        ;
      }
      if (*(int *)(*(int *)(param_1 + 0x1c) + 0x38) != 0) {
        (**(code **)(param_1 + 0x24))
                  (*(undefined4 *)(param_1 + 0x28),*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x38))
        ;
      }
      if (*(int *)(*(int *)(param_1 + 0x1c) + 0x30) != 0) {
        (**(code **)(param_1 + 0x24))
                  (*(undefined4 *)(param_1 + 0x28),*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x30))
        ;
      }
      (**(code **)(param_1 + 0x24))(*(undefined4 *)(param_1 + 0x28),*(undefined4 *)(param_1 + 0x1c))
      ;
      *(undefined4 *)(param_1 + 0x1c) = 0;
      uVar2 = (iVar1 != 0x71) - 1 & 0xfffffffd;
    }
    else {
      uVar2 = 0xfffffffe;
    }
  }
  return uVar2;
}

