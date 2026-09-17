
void FUN__text__00552c75(int *param_1)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)(**(code **)param_1[1])(param_1,1,0x58);
  param_1[0x69] = (int)puVar1;
  puVar1[0x11] = 0;
  puVar1[0xd] = 0;
  *puVar1 = FUN__text__00552b96;
  puVar1[2] = &DAT__text__00552c60;
  puVar1[3] = &LAB__text__00552c61;
  if (4 < param_1[0x19]) {
    *(undefined4 *)(*param_1 + 0x14) = 0x36;
    *(undefined4 *)(*param_1 + 0x18) = 4;
    (**(code **)*param_1)(param_1);
  }
  if (0x100 < param_1[0x15]) {
    *(undefined4 *)(*param_1 + 0x14) = 0x38;
    *(undefined4 *)(*param_1 + 0x18) = 0x100;
    (**(code **)*param_1)(param_1);
  }
  FUN__text__0055235e();
  FUN__text__0055248b(param_1);
  if (param_1[0x13] == 2) {
    FUN__text__00552b60();
  }
  return;
}

