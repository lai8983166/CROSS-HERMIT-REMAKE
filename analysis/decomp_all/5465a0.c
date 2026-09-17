
void FUN__text__005465a0(int param_1,undefined4 param_2,undefined4 param_3)

{
  *(undefined4 *)(param_1 + 0x54) = param_2;
  *(undefined4 *)(param_1 + 0x50) = param_3;
  if (*(int *)(param_1 + 0x4c) != 0) {
    *(undefined4 *)(param_1 + 0x4c) = 0;
    FUN__text__0054383b(param_1,"It\'s an error to set both read_data_fn and write_data_fn in the ")
    ;
    FUN__text__0054383b(param_1,"same structure.  Resetting write_data_fn to NULL.");
  }
  *(undefined4 *)(param_1 + 0x120) = 0;
  return;
}

