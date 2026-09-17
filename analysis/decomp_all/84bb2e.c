
void FUN__text1__0084bb2e(undefined **param_1)

{
  VirtualFree(param_1[4],0,0x8000);
  if ((undefined **)PTR_LOOP_008725c8 == param_1) {
    PTR_LOOP_008725c8 = param_1[1];
  }
  if (param_1 != &PTR_LOOP_008705a8) {
    *(undefined **)param_1[1] = *param_1;
    *(undefined **)(*param_1 + 4) = param_1[1];
    HeapFree(DAT_00876b40,0,param_1);
    return;
  }
  DAT_008705b8 = 0xffffffff;
  return;
}

