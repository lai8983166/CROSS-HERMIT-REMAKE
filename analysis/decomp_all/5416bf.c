
undefined4 FUN__text__005416bf(int *param_1)

{
  if ((param_1[4] < 200) || (0xd2 < param_1[4])) {
    *(undefined4 *)(*param_1 + 0x14) = 0x12;
    *(int *)(*param_1 + 0x18) = param_1[4];
    (**(code **)*param_1)(param_1);
  }
  return CONCAT31((int3)((uint)param_1[99] >> 8),*(undefined1 *)(param_1[99] + 0x11));
}

