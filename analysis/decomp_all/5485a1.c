
undefined4 __fastcall FUN__text__005485a1(int param_1)

{
  if (*(int *)(param_1 + 0x60) == 0) {
    return 0x8876086c;
  }
  (**(code **)(**(int **)(param_1 + 4) + 0xd8))
            (*(int **)(param_1 + 4),*(undefined4 *)(param_1 + 100));
  (**(code **)(**(int **)(param_1 + 0xc) + 0x1c))(*(int **)(param_1 + 0xc));
  *(undefined4 *)(param_1 + 0x60) = 0;
  return 0;
}

